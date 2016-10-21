## INFO ##
## INFO ##

# Import templang modules
from parser      import (Literal,
                         Attribute)
from interpreter import (UnknownAttribute,
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
            strings.append(states.evaluate(expression))

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
            [end <END>]
            [sep <SEPARATOR>]
    """
    _print(element, states, states.stdout)



#------------------------------------------------------------------------------#
def write(element,
          states):
    """
    Write to output document
    Usage:
        ($write <INPUTS> <OPTIONS>)
        OPTIONS:
            [end <END>]
            [sep <SEPARATOR>]
    """
    _print(element, states, states.output)



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    '$print'     : print_,
    '$write'     : write
}
