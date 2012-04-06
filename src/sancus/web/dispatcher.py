from webob.exc import HTTPNotFound

class PathMapper(object):
    def __call__(self, environ, start_response):
        raise HTTPNotFound()
