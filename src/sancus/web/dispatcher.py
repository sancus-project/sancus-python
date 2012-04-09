from webob.exc import HTTPNotFound

from .urltemplate import URLTemplateCompiler

import re
import logging

_logger = logging.getLogger(__name__)

class WSGIMapper(object):
    """
    """
    def __init__(self, logger=_logger):
        """
        """
        self.logger = logger
        self.patterns = []

    def __call__(self, environ, start_response):
        """
        """
        (h, args) = self.find_handler(environ)

        if 'wsgiorg.routing_args' not in environ:
            environ['wsgiorg.routing_args'] = ((), {})

        environ['wsgiorg.routing_args'][1].update(args)

        if isinstance(h, type):
            h = h(environ)

        return h(environ, start_response)

    def find_handler(self, environ):
        """
        """
        raise HTTPNotFound()

    def compile(self, expr):
        """
        """
        return re.compile(expr)

    def add(self, expr, h, **kw):
        """
        """
        self.logger.debug('add(%r, %r, %r)' % (expr, h, kw))

        p = (self.compile(expr), (h, kw))
        self.patterns.append(p)

class PathMapper(WSGIMapper):
    """
    """
    compile = URLTemplateCompiler()
    match = compile.match

    def find_handler(self, environ):
        """
        """
        script_name = environ.get('SCRIPT_NAME', '')
        path_info = environ.get('PATH_INFO', '')

        # find first good match
        for regex, handler in self.patterns:
            match, pos_args, named_args, matched_path_info, extra_path_info = self.match(regex, path_info)
            if not match:
                continue
            elif extra_path_info and not extra_path_info.startswith('/'):
                continue

            cur_pos, cur_named = environ.get('wsgiorg.routing_args', ((), {}))
            new_pos = list(cur_pos) + list(pos_args)
            new_named = cur_named.copy()
            new_named.update(named_args)

            environ['wsgiorg.routing_args'] = (cur_pos, new_named)
            environ['SCRIPT_NAME'] = script_name + matched_path_info
            environ['PATH_INFO'] = extra_path_info

            self.logger.debug("%s %s (%s?%s) %r",
                    environ['REQUEST_METHOD'], environ['SCRIPT_NAME'],
                    environ['PATH_INFO'], environ['QUERY_STRING'],
                    handler)

            return handler

        raise HTTPNotFound()
