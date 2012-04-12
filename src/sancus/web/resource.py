from webob import Request, Response
import webob.exc as exc

class Resource(Response):
    _methods = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE')

    def supported_methods(self):
        """
        """
        try:
            return type(self)._supported_methods
        except:
            l = []

        for method in self._methods:
            # no 'HEAD' if no 'GET'
            if method == 'HEAD' and 'GET' not in l:
                continue

            # self.FOO must exist and be callable
            if callable(getattr(self, method, None)):
                l.append(method)

        type(self)._supported_methods = l
        return l

    def HEAD(self, req, *d, **kw):
        return self.GET(req, *d, **kw)

    def __init__(self, environ, *d, **kw):
        """
        """

        # method
        method = environ['REQUEST_METHOD']
        if method not in self.supported_methods():
            raise exc.HTTPMethodNotAllowed(allow = self.supported_methods())

        # handler
        handler_name = method
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
        self.allow = self.supported_methods()

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
            raise exc.HTTPMethodNotAllowed(allow = self.supported_methods())
        elif ret == 400:
            raise exc.HTTPBadRequest()
        elif ret == 503:
            raise exc.HTTPServiceUnavailable()
        else:
            assert "handler %s returned %r" % (hn, ret)
