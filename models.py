from mongoengine import *
from datetime import datetime
from diff_match_patch import diff_match_patch

class Revision(EmbeddedDocument):
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
		patches = [diff.patch_fromText(revision.content) for revision in self.revisions[1:][0:index]]
		if patches==[]:
			print 'WHAT!'
			return self.revisions[index].content
		else:
			return diff.patch_apply(patches, self.revisions[0])[0]
	
	@property
	def current_revision(self):
		return self._get_revision(-1)
	
	@property
	def all_revisions(self):
		return (self._get_revision(i) for i,val in enumerate(self.revisions))

	def save(self, *args, **kwargs):
		'''
		I'd like to override this to automatically save the diffs of new revisions instead of
		full content, but I'm blanking on how. TO DO
		'''
		if len(self.revisions) > 1:
			diff = diff_match_patch()
			patch = diff.patch_make(self._get_revision(-2), self.current_revision)
			self.revisions[-1].content = diff.patch_toText(patch)
		super(Entry, self).save(*args, **kwargs)

if __name__=='__main__':
	from mongoengine import connect
	connect('test')
	entry = Entry()
	entry.revisions.append(Revision(content='hello', rows=1))
	entry.save()
	entry.revisions.append(Revision(content='hello\n', rows=1))
	entry.save()
	print entry.current_revision
	print entry.revisions[1:][0:(-1+1)]
