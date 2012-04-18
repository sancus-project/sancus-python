from .resource import Resource
import webob.exc as exc

collection_methods = {
    'GET': 'LIST',
    'POST': 'CREATE',
    }

item_methods = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE')

class Collection(Resource):
    __itemid__ = 'id'

    def supported_methods(self, environ):
        """
        """
        try:
            return self._supported_methods
        except:
            pass

        try:
            item = environ['wsgiorg.routing_args'][1][self.__itemid__]
        except:
            item = None

        cls = type(self)
        if item:
            try:
                l = cls._item_methods
            except:
                l = self.find_supported_methods(item_methods)
                cls._item_methods = l
        else:
            try:
                l = cls._collection_methods
            except:
                l = self.find_supported_methods(collection_methods)
                cls._collection_methods = l

        self._supported_methods = l
        return l
