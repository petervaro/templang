## INFO ##
## INFO ##

# Import python modules
from importlib import import_module

# Import templlang modules
from error  import TempLangError
from parser import parse, Element, Attribute, Literal


#------------------------------------------------------------------------------#
class InterpreterError(TempLangError): pass
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnknownAttribute(InterpreterError):
    MESSAGE = 'Unknown attribute'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnknownKeyword(InterpreterError):
    MESSAGE = 'Unknown keyword'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidAttributeParameter(InterpreterError):
    MESSAGE = 'Invalid attribute option'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class TooFewAttributeParameter(InvalidAttributeParameter):
    MESSAGE = 'Too few attribute parameters'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class TooManyAttributeParameters(InvalidAttributeParameter):
    MESSAGE = 'Too many attribute parameters'



#------------------------------------------------------------------------------#
def _element_eval(element, states):
    try:
        result = states.ELEM_KEYWORDS[element.value](element, states)
        return '' if result is None else result
    except KeyError:
        raise UnknownKeyword(element.report)



#------------------------------------------------------------------------------#
def _attribute_eval(attribute, states):
    try:
        states.ATTR_KEYWORDS[attribute.value](attribute, states)
    except KeyError:
        raise UnknownAttribute(attribute.report)



#------------------------------------------------------------------------------#
def _literal_eval(element, states):
    pass



#------------------------------------------------------------------------------#
def _use(attribute, states):
    for package_name in attribute:
        module = import_module('packages.' + package_name.value)
        for attr in ('ROOT_BEHAVIOR',
                     'ATTR_KEYWORDS',
                     'ELEM_KEYWORDS'):
            try:
                getattr(states, attr).update(getattr(module, attr))
            except AttributeError:
                pass



#------------------------------------------------------------------------------#
class InterpreterStates:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def output(self):
        return self._output


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def element_eval(self):
        return self._root_behavior['element']


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def attribute_eval(self):
        return self._root_behavior['attribute']


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def literal_eval(self):
        return self._literal_eval['literal']


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def ROOT_BEHAVIOR(self):
        return self._root_behavior


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def ATTR_KEYWORDS(self):
        return self._attr_keywords


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def ELEM_KEYWORDS(self):
        return self._elem_keywords


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, root,
                       output):
        self._root          = root
        self._output        = output
        self._elem_keywords = {}
        self._attr_keywords = {'use' : _use}
        self._root_behavior = {'element'   : _element_eval,
                               'attribute' : _attribute_eval,
                               'literal'   : _literal_eval}



#------------------------------------------------------------------------------#
def interpret(path  : str,
              source: 'file',
              output: 'file'):
    root   = parse(path, source.read())
    states = InterpreterStates(root, output)
    for expression in root:
        if isinstance(expression, Element):
            states.element_eval(expression, states)
        elif isinstance(expression, Attribute):
            states.attribute_eval(expression, states)
        elif isinstance(expression, Literal):
            states.literal_eval(expression, states)
