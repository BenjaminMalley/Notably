from flask import Flask

for method in ['get', 'head', 'post', 'put', 'delete', 'options']:
	if method in Flask.__dict__.keys():
		raise ImportWarning("{0} attribute already present.".format(method))
	setattr(Flask, method, lambda self, url: self.route(url, methods=[method]))