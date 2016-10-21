## INFO ##
## INFO ##

from .html5 import tag, ELEM_KEYWORDS

ELEM_KEYWORDS[NotImplemented] = lambda *a, **kw: tag(*a, **kw)
