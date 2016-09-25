## INFO ##
## INFO ##

# Import templang modules
from error       import TempLangError
from parser      import (Literal,
                         Attribute)
from interpreter import (interpret,
                         UnknownKeyword,
                         UnexpectedExpressionType,
                         UnknownAttributeForElement,
                         ElementParameterTypeError)


#------------------------------------------------------------------------------#
# Module level internal constant
_EXPORTED = []



#------------------------------------------------------------------------------#
class FileNotFound(TempLangError):
    MESSAGE = 'File not found'



# Helper functions
#------------------------------------------------------------------------------#
def _get_path_from_attrs(element):
    for expression in element:
        if isinstance(expression, Attribute):
            if expression.value == 'path':
                for literal in expression:
                    yield literal
            else:
                raise UnknownAttributeForElement(expression.report)
        else:
            raise UnexpectedExpressionType(expression.report)



# Keyword functions
#------------------------------------------------------------------------------#
# TODO: Make `import` recursion proof!
def import_(element,
            states):
    """
    Import other .tl file(s) and evaluate them.
    The extension can be omitted.
    Usage:
        ($import [path {<PATH1>} {<PATH2>} {<PATH..>}]) or
        ($import [path {<PATH1>}]
                 [path {<PATH2>}]
                 [path {<PATH..>}])
    """
    for path_literal in _get_path_from_attrs(element):
        path   = path_literal.value
        export = {}
        _EXPORTED.append(export)
        if not path.endswith('.tl'):
            path += '.tl'
        try:
            with open(path) as file:
                interpret(path, file, states.output)
                for keyword, callback in export.items():
                    try:
                        states.add_element(keyword, callback)
                    except KeyError:
                        raise
        except FileNotFoundError:
            raise FileNotFound(path_literal.report)
        _EXPORTED.pop()



#------------------------------------------------------------------------------#
def export(element,
           states):
    """
    Export elements, which can be imported later on.
    Usage:
        ($export <KEYWORD1> <KEYWORD2> <KEYWORD...>)
    """
    try:
        export = _EXPORTED[-1]
    except IndexError:
        return
    for expression in element:
        keyword = states.evaluate(expression)
        if not isinstance(keyword, str):
            raise ElementParameterTypeError(expression.report)
        try:
            export[keyword] = states.ELEM_KEYWORDS[keyword]
        except KeyError:
            raise UnknownKeyword(expression.report)



#------------------------------------------------------------------------------#
def include(element,
            states):
    """
    Include other text file(s) as Literal.
    Usage:
        ($include [path {<PATH1>} {<PATH2>} {<PATH..>}]) or
        ($include [path {<PATH1>}]
                  [path {<PATH2>}]
                  [path {<PATH..>}])
    """
    result = Literal(None)
    for path_literal in _get_path_from_attrs(element):
        try:
            with open(path_literal.value) as file:
                result += file.read()
        except FileNotFoundError:
            raise FileNotFound(path_literal.report)
    return result



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    '$import' : import_,
    '$export' : export,
    'include' : include,
}
