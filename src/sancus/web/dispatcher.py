from webob.exc import HTTPNotFound

class WSGIMapper(object):
    def __call__(self, environ, start_response):
        (h, args) = self.find_handler(environ)

        if 'wsgiorg.routing_args' not in environ:
            environ['wsgiorg.routing_args'] = ((), {})

        environ['wsgiorg.routing_args'][1].update(args)

        if isinstance(h, type):
            h = h(environ)

        return h(environ, start_response)

    def find_handler(self, environ):
        raise HTTPNotFound()

class PathMapper(WSGIMapper):
    pass
