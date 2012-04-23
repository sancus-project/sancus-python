# -*- coding: utf-8 -*-

from pprint import pformat, pprint

class Table(object):
    """
    Like a Lua table, where items and attributes are the same thing, and
    setting them to None deletes them
    """

    def __init__(self, **kw):
        # remove None entries, and avoid self._fields recursion
        d = dict((k,v) for k,v in kw.iteritems() if v is not None)
        object.__setattr__(self, '_fields', d)

    def __repr__(self):
        d = ["%s = %r" % (k,v) for k,v in self._fields.iteritems()]
        return "Table(%s)" % ', '.join(d)

    def __iter__(self):
        return self._fields.iteritems()

    def __len__(self):
        return len(self._fields)

    def __delitem__(self, key):
        del self._field[key]

    def __getattr__(self, key):
        return self._fields.get(key, None)

    def __getitem__(self, key):
        return self._fields.get(key, None)

    def __contains__(self, key):
        return key in self._fields

    def __setattr__(self, key, value):
        if value is not None:
            self._fields[key] = value
        else:
            try:
                del self._fields[key]
            except KeyError:
                pass

    def __setitem__(self, key, value):
        if value is not None:
            self._fields[key] = value
        else:
            try:
                del self._fields[key]
            except KeyError:
                pass
