from mongoengine import *
from datetime import datetime
from diff_match_patch import diff_match_patch

class Revision(EmbeddedDocument):
	'''
	Each Entry has a ListField containing diffs for all the revisions, ordered by date.
	'''
	content = StringField()
	date = DateTimeField(default=datetime.now())
	rows = IntField()

class Entry(Document):
	'''
	Entry tracks a list of revisions.  The first revision, revisions[0], is the content the user submits
	at the time Entry is created.  For every subsequent revision, we just append the diff as computed by
	Google's diff-match-patch.  Thus, when we need to restore an arbitrary revision, we have to build it back
	from the first revision.
	'''
	author = StringField(default='None')
	visible = BooleanField(default=True)	
	public = BooleanField(default=False)	 
	revisions = ListField(EmbeddedDocumentField(Revision))

	def _get_revision(self, index):
		diff = diff_match_patch()
		# append zero to the array so that a slice with negative indices can retrieve the last element
		patches = [diff.patch_fromText(revision.content)[0] for revision in (self.revisions+[0])[1:index]]
		if patches==[]: #no patches to apply
			return self.revisions[index].content
		else:
			return diff.patch_apply(patches, self.revisions[0].content)[0]
	
	@property
	def current_revision(self):
		return self._get_revision(-1)
		
	@property
	def all_revisions(self):
		return (self._get_revision(i) for i,val in enumerate(self.revisions))

	def add_revision(self, revision):
		'''Call this instead of append to add a document revision'''
		if len(self.revisions) >= 1:
			# convert latest revision into a diff before saving
			diff = diff_match_patch()
			patch = diff.patch_make(self.current_revision, revision.content)
			revision.content = diff.patch_toText(patch)
			self.revisions.append(revision)
		else:
			#save the first revision as a full text doc
			self.revisions.append(revision)
