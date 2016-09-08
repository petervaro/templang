## INFO ##
## INFO ##

# Import python modules
from sys import stdout

# Import templang modules
from parser import Attribute, Literal
from interpreter import (interpret,
                         UnknownAttribute,
                         TooFewAttributeParameter,
                         TooManyAttributeParameters)


#------------------------------------------------------------------------------#
# Helper functions
def _print_set_option(option,
                      options,
                      values,
                      report):
    try:
        value, _, *rest = values
        raise TooManyAttributeParameters(report)
    except ValueError:
        try:
            value, = values
            options[option] = value.value
        except ValueError:
            #  options[option] = ''
            raise TooFewAttributeParameter(report)



#------------------------------------------------------------------------------#
# Internal module level constants
_PRINT_OPTIONS = {
    'sep' : lambda *a, **kw: _print_set_option('sep', *a, **kw),
    'end' : lambda *a, **kw: _print_set_option('end', *a, **kw)
}
_REPLACE_CHARACTERS = {
    '\\n' : '\n'
}



#------------------------------------------------------------------------------#
def _print(element,
           states,
           stream):
    strings = []
    options = {'sep' : ' ',
               'end' : '\n'}
    for expression in element:
        if isinstance(expression, Attribute):
            try:
                _PRINT_OPTIONS[expression.value](options,
                                                 expression,
                                                 expression.report)
            except KeyError:
                raise UnknownAttribute(expression.report)
        elif isinstance(expression, Literal):
            strings.append(expression.value)
        else:
            strings.append(states.element_eval(expression, states))

    print(*strings, **options, file=stream)



#------------------------------------------------------------------------------#
# Keyword functions
def print_(element,
           states):
    """
    Print to console
    Usage:
        ($print <INPUTS> <OPTIONS>)
        OPTIONS:
            [end {<END>}]
            [sep {<SEPARATOR>}]
    """
    _print(element, states, stdout)



#------------------------------------------------------------------------------#
def write(element,
          states):
    """
    Write to output document
    Usage:
        ($write <INPUTS> <OPTIONS>)
        OPTIONS:
            [end {<END>}]
            [sep {<SEPARATOR>}]
    """
    _print(element, states, states.output)



#------------------------------------------------------------------------------#
def to_string(element,
              states):
    """
    Usage:
        ($to-string <INPUTS>)
    """
    return ' '.join(map(str, element))



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    '$print'     : print_,
    '$write'     : write,
    '$to-string' : to_string
}
