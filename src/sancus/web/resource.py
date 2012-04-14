from webob import Request, Response
import webob.exc as exc

class Resource(Response):
    _methods = ('GET', 'POST', 'PUT', 'DELETE')

    def find_supported_methods(self, d):
        if isinstance(d, tuple):
            l = dict((m, m) for m in d if callable(getattr(self, m, None)))
        else:
            l = dict((m, h) for (m, h) in d.items() if callable(getattr(self, h, None)))

        if 'GET' in l and not 'HEAD' in l:
            l['HEAD'] = l['GET']

        return l

    def supported_methods(self, environ=None):
        """
        """
        try:
            return type(self)._supported_methods
        except:
            l = self.find_supported_methods(self._methods)

        type(self)._supported_methods = l
        return l

    def __init__(self, environ, *d, **kw):
        """
        """
        # method
        handlers = self.supported_methods(environ)
        try:
            handler_name = handlers[environ['REQUEST_METHOD']]
        except:
            raise exc.HTTPMethodNotAllowed(allow = handlers)

        # handler
        handler = getattr(self, handler_name, None)
        if not handler:
            raise exc.HTTPNotFound()

        environ['sancus.handler_name'] = handler_name
        environ['sancus.handler'] = handler

        # arguments
        pos_args, named_args = environ.get('wsgiorg.routing_args', ((), {}))
        named_args = dict((k, v) for k, v in named_args.iteritems() if v is not None)

        environ['sancus.pos_args'] = pos_args
        environ['sancus.named_args'] = named_args

        # webob
        req = Request(environ)
        Response.__init__(self, *d, request=req, **kw)
        self.allow = handlers

    def __call__(self, environ, start_response):
        d = environ['sancus.pos_args']
        kw = environ['sancus.named_args']
        h = environ['sancus.handler']
        hn = environ['sancus.handler_name']

        ret = h(self.request, *d, **kw)
        if ret is None:
            return Response.__call__(self, environ, start_response)
        elif ret == 404:
            raise exc.HTTPNotFound()
        elif ret == 405:
            raise exc.HTTPMethodNotAllowed(allow = self.supported_methods(environ))
        elif ret == 400:
            raise exc.HTTPBadRequest()
        elif ret == 503:
            raise exc.HTTPServiceUnavailable()
        else:
            assert "handler %s returned %r" % (hn, ret)
