## INFO ##
## INFO ##

# Import python modules
from re import compile

# Import templang modules
from parser      import Attribute
from interpreter import (UnknownAttributeForElement,
                         AttributeParameterTypeError,
                         ElementParameterTypeError)


#------------------------------------------------------------------------------#
# Module level internal constants
_FORMAT_ESCAPE  = {'%%', '%'}
_FORMAT_VALID   = compile(r'(?<!%)%(?P<index>\d+)')
_FORMAT_ILLEGAL = compile(r'')


#------------------------------------------------------------------------------#
def join(element,
         states):
    """
    ($join <VALUE1> <VALUE2> <VALUE...>) or
    ($join <VALUE1> <VALUE2> <VALUE...> [sep <SEPARATOR>])
    """
    sep    = ''
    values = []
    for expression in element:
        if isinstance(expression, Attribute):
            if expression.value == 'sep':
                sep = states.evaluate(expression)
                if not isinstance(sep, str):
                    raise AttributeParameterTypeError(expression.report)
            else:
                raise UnknownAttributeForElement(expression.report)
        else:
            value = states.evaluate(expression)
            if isinstance(value, str):
                values.append(value)
            else:
                raise ElementParameterTypeError(expression.report)
    return sep.join(values)



#------------------------------------------------------------------------------#
def format_(element,
            states):
    """
    Usage:
        (format [% <SPECIFIER>] <VALUE1> <VALUE2> <VALUE...>)
    Specifier:
        %<index>
    """




#------------------------------------------------------------------------------#
def to_string(element,
              states):
    """
    Usage:
        (to-string <VALUE1> <VALUE2> <VALUE...>)
    """
    return ' '.join(map(str, element))



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    'join'       : join,
    'format'     : format_,
    'to-string'  : to_string
}
