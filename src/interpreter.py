## INFO ##
## INFO ##

# Import python modules
from random    import choice
from importlib import import_module
from string    import ascii_letters, digits

# Import templlang modules
from error  import TempLangError
from parser import parse, Expression, Element, Attribute, Literal



#------------------------------------------------------------------------------#
class InterpreterError(TempLangError): pass
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedExpressionType(InterpreterError):
    MESSAGE = 'Unexpected expression type'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnknownAttribute(InterpreterError):
    MESSAGE = 'Unknown attribute'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnknownKeyword(InterpreterError):
    MESSAGE = 'Unknown keyword'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnknownAttributeForElement(InterpreterError):
    MESSAGE = 'Unknown attribute for element'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidAttributeParameter(InterpreterError):
    MESSAGE = 'Invalid attribute option'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidExpressionForElement(InterpreterError):
    MESSAGE = 'Invalid expression for element'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class TooFewAttributeParameter(InvalidAttributeParameter):
    MESSAGE = 'Too few attribute parameters'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class TooManyAttributeParameters(InvalidAttributeParameter):
    MESSAGE = 'Too many attribute parameters'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class ElementParameterTypeError(InvalidAttributeParameter):
    MESSAGE = 'Invalid parameter type for element'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class AttributeParameterTypeError(InvalidAttributeParameter):
    MESSAGE = 'Invalid parameter type for attribute'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class TooFewExpressionsForElement(InvalidExpressionForElement):
    MESSAGE = 'Too few expressions for element'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class TooManyExpressionsForElement(InvalidExpressionForElement):
    MESSAGE = 'Too many expression for element'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class MissingPackage(InterpreterError):
    MESSAGE = 'Package is missing'



#------------------------------------------------------------------------------#
class Scope:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def parent(self):
        return self._parent


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, parent        = None,
                       elem_keywords = None,
                       attr_keywords = None):
        self._parent        = parent
        self._elem_keywords = elem_keywords or {}
        self._attr_keywords = attr_keywords or {}


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add_element(self, keyword,
                          callback):
        self._elem_keywords[keyword] = callback


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def eval_element(self, element,
                           states):
        # If element is defined in the current scope
        try:
            result = self._elem_keywords[element.value](element, states)
        except KeyError:
            # If element is defined in parent scope
            try:
                result = self._parent.eval_element(element, states)
            # If element is None
            except AttributeError:
                raise UnknownKeyword(element.report)

        # If result is None or empty string
        if not result:
            return ''
        # If result is an expression needs to be evaluated
        elif isinstance(result, Expression):
            return states.evaluate(result)
        # If result is string
        elif isinstance(result, str):
            return result
        # If result is something else
        else:
            raise TypeError('Unknown result type for '
                            'eval_element: {}'.format(result.__class__.__name__))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def eval_attribute(self, attribute,
                             states):
        try:
            self._attr_keywords[attribute.value](attribute, states)
        except KeyError:
            raise UnknownAttribute(attribute.report)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def eval_literal(self, literal,
                           states):
        return literal.value



#------------------------------------------------------------------------------#
class InterpreterStates:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @staticmethod
    def _use(attribute,
             states):
        for package_expr in attribute:
            package_name = states.evaluate(package_expr)
            try:
                module = import_module('packages.' + package_name)
            except ImportError:
                raise MissingPackage(package_expr.report)
            for attr in ('ATTR_KEYWORDS',
                         'ELEM_KEYWORDS'):
                try:
                    getattr(states, attr).update(getattr(module, attr))
                except AttributeError:
                    pass


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @staticmethod
    def _empty(element,
               states):
        result = None
        for expression in element:
            result = states.evaluate(expression)
        return result


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def output(self):
        return self._output


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def ATTR_KEYWORDS(self):
        return self._scope._attr_keywords


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def ELEM_KEYWORDS(self):
        return self._scope._elem_keywords


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, root,
                       output):
        self._root   = root
        self._output = output
        self._scope  = Scope(elem_keywords = {'' : self._empty},
                             attr_keywords = {'use' : self._use})


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add_element(self, *args, **kwargs):
        self._scope.add_element(*args, **kwargs)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def evaluate(self, expression):
        for type, attr in ((Element  , 'eval_element'),
                           (Attribute, 'eval_attribute'),
                           (Literal  , 'eval_literal')):
            if isinstance(expression, type):
                return getattr(self._scope, attr)(expression, self)
        raise TypeError('Unknown expression type:' +
                        expression.__class__.__name__)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def scope(self, evaluator):
        def wrapped(*args, **kwargs):
            # Open new scope
            self._scope = Scope(self._scope)
            # Evaluate expressions
            result = evaluator(*args, **kwargs)
            # Close scope
            self._scope = self._scope.parent
            # Return evaluated result
            return result
        return wrapped



#------------------------------------------------------------------------------#
def interpret(text   : str,
              source : 'file',
              output : 'file'):
    root   = parse(text, source.read())
    states = InterpreterStates(root, output)
    for expression in root:
        states.evaluate(expression)
