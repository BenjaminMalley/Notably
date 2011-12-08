from flask import Flask

for method in ('get', 'head', 'post', 'put', 'delete', 'options'):
	if method in Flask.__dict__.keys():
		raise ImportWarning("{0} attribute already present.".format(method))
	def route_decorator(self, url):
		def wrapper(*args, **kwargs):
			kwargs.update({'METHODS': [method.upper()]})
			return wrapper
	setattr(Flask, method, route_decorator)
	