## INFO ##
## INFO ##

# Import python modules
from re import compile, finditer

# Import templang modules
from parser      import Attribute
from interpreter import (InterpreterError,
                         UnknownAttributeForElement,
                         AttributeParameterTypeError,
                         ElementParameterTypeError,
                         TooFewAttributeParameter,
                         TooManyAttributeParameters)


#------------------------------------------------------------------------------#
# Module level internal constants
_FORMAT_VALID   = compile(r'(?<!%)%((?P<index>\d+)|(?P<next>\?))')


#------------------------------------------------------------------------------#
class FormatIndexOutOfRange(InterpreterError):
    MESSAGE = 'Index in format specifier is out of range'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class FormatArgumentTypeError(InterpreterError):
    MESSAGE = 'Argument is not a literal'


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
        %?   - substitute with next argument
        %<i> - substitute argument at i (where i starts from 0)
    """
    specifiers = ''
    arguments  = []
    for expression in element:
        if isinstance(expression, Attribute):
            if expression.value == '%':
                try:
                    specifier_expr, *rest = expression
                    if rest:
                        raise TooManyAttributeParameters(expression.report)
                except ValueError:
                    raise TooFewAttributeParameter(expression.report)
                specifier = states.evaluate(specifier_expr)
                if not isinstance(specifier, str):
                    raise AttributeParameterTypeError(specifier_expr.report)
                specifiers += specifier
            else:
                raise UnknownAttributeForElement(expression.report)
        else:
            arguments.append(states.evaluate(expression))

    i = 0
    result = ''
    iarguments = iter(arguments)
    try:
        for match in finditer(_FORMAT_VALID, specifiers):
            result += specifier[i:match.start()]
            i = match.end()
            group = match.group('index')
            if group:
                substring = arguments[int(group)]
            else:
                substring = next(iarguments)
            result += substring
        result += specifiers[i:]
    except (IndexError, StopIteration):
        raise FormatIndexOutOfRange(element.report)
    except TypeError:
        raise FormatArgumentTypeError(substring.report)

    return result



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
