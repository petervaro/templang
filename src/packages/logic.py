## INFO ##
## INFO ##

# Import templang modules
from error       import TempLangError
from parser      import (Literal,
                         Attribute)
from interpreter import (UnknownAttributeForElement,
                         InvalidExpressionForElement,
                         TooFewAttributeParameter,
                         TooManyAttributeParameters,
                         AttributeParameterTypeError,
                         TooFewExpressionsForElement,
                         TooManyExpressionsForElement)

#------------------------------------------------------------------------------#
# Module level internal constants
_DEFINITIONS = {}



#------------------------------------------------------------------------------#
class UndefinedVariable(TempLangError):
    MESSAGE = 'Variable is undefined in this scope'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnknownMixinArgument(TempLangError):
    MESSAGE = 'Unknown argument for mixin'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class MissingMixinName(TempLangError):
    MESSAGE = 'Name of mixin is missing'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidMixinNameType(TempLangError):
    MESSAGE = "Mixin name's type must be Literal"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidVariableNameType(TempLangError):
    MESSAGE = "Variable name's type must be Literal"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class EmptyVariableName(TempLangError):
    MESSAGE = 'Variable name cannot be empty Literal'
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class MixinArgumentAlreadyDefined(TempLangError):
    MESSAGE = 'Mixin argument already defined'



#------------------------------------------------------------------------------#
def define(element,
           states):
    """
    Definitions are global and module idependent.
    ($define '<NAME>') or
    ($define '<NAME>' <VALUE>)
    """
    name  = ''
    value = None

    for expression in element:
        if isinstance(expression, Attribute):
            raise UnknownAttributeForElement(expression.report)
        elif not name:
            name = states.evaluate(expression)
            if not name:
                raise InvalidExpressionForElement(expression.report)
        elif value is None:
            value = states.evaluate(expression)
        else:
            raise InvalidExpressionForElement(expression.report)

    _DEFINITIONS[name] = '' if value is None else value



#------------------------------------------------------------------------------#
def undefine(element,
             states):
    """
    ($undefine '<NAME>')
    """
    name = None
    for expression in element:
        if isinstance(expression, Attribute):
            raise UnknownAttributeForElement(expression.report)
        elif name is None:
            name = states.evaluate(expression)
        else:
            raise InvalidExpressionForElement(expression.report)

    _DEFINITIONS.pop(name, None)



#------------------------------------------------------------------------------#
def is_defined(element,
               states):
    pass



#------------------------------------------------------------------------------#
def expose(element,
           states):
    """
    ($expose '<NAME>')
    """
    name = None
    for expression in element:
        if isinstance(expression, Attribute):
            raise UnknownAttributeForElement(expression.report)
        elif name is None:
            name = states.evaluate(expression)
        else:
            raise InvalidExpressionForElement(expression.report)

    return _DEFINITIONS.get(name, '')



#------------------------------------------------------------------------------#
def _eval_var(result):
    def eval_var(element,
                 states):
        # If assignment
        try:
            value, *rest = element
            if rest:
                raise TooManyExpressionsForElement(rest[0].report)
            result[0] = states.evaluate(value)
        # If look-up
        except ValueError:
            return result[0]
    return eval_var



#------------------------------------------------------------------------------#
def _get_value(expression):
    if isinstance(expression, Literal):
        return expression
    try:
        value, *rest = expression
    except ValueError:
        raise TooFewAttributeParameter(expression.report)
    if rest:
        raise TooManyAttributeParameters(rest[0].report)
    return value



#------------------------------------------------------------------------------#
def var(element,
        states):
    """
    Variables are scope agnostic.
    ($var '<NAME>' <VALUE>)
    """

    try:
        name_expr, value_expr, *rest = element
        if rest:
            raise TooManyExpressionsForElement(rest[0].report)
    except ValueError:
        raise TooFewExpressionsForElement(element.report)

    name = states.evaluate(name_expr)
    if isinstance(name, str):
        if not name:
            raise EmptyVariableName(name_expr.report)
    else:
        raise InvalidVariableNameType(name_expr.report)

    states.add_element(name, _eval_var([states.evaluate(value_expr)]))



#------------------------------------------------------------------------------#
def mixin(element,
          states):
    """
    Creates a mixin in the current scope.
    Evaluating the mixin will return its last expression.
    Usage:
        ($mixin [name '<NAME>']
                [args '<ARG1>' '<ARG2>']
                [xarg '<XARG1>']
                [xarg '<XARG2>' <DEFAULT>]
            <ELEMENTS>)
    """
    name_expr = None
    args      = []
    xargs     = {}
    exprs     = []

    for expression in element:
        # Set attributes of the mixin
        if isinstance(expression, Attribute):
            # If defining the name of the mixin
            if expression.value == 'name':
                try:
                    name_expr, *rest = expression
                    if rest:
                        raise TooManyAttributeParameters(name_expr.report)
                except ValueError:
                    TooFewAttributeParameter(expression.report)

            # If defining the arguments of the mixin
            elif expression.value == 'args':
                for arg_expr in expression:
                    arg = states.evaluate(arg_expr)
                    if not arg:
                        raise EmptyVariableName(arg_expr.report)
                    elif isinstance(arg, str):
                        if arg in args:
                            raise MixinArgumentAlreadyDefined(arg_expr.report)
                        args.append(arg)
                    else:
                        raise AttributeParameterTypeError(arg_expr.report)

            # If defining the extra arguments of the mixin
            elif expression.value == 'xarg':
                try:
                    xarg_expr, *default = expression
                    if len(default) > 1:
                        raise TooManyAttributeParameters(default[1].report)
                except ValueError:
                    raise TooFewAttributeParameter(expression.report)

                xarg = states.evaluate(xarg_expr)
                if not xarg:
                    raise EmptyVariableName(xarg_expr.report)
                elif isinstance(xarg, str):
                    if xarg in xargs:
                        raise MixinArgumentAlreadyDefined(xarg_expr.report)
                    xargs[xarg] = states.evaluate(default[0]) if default else ''
                else:
                    raise AttributeParameterTypeError(xarg_expr.report)

            # Unknown attribute
            else:
                raise UnknownAttributeForElement(expression.report)
        # Collect expressions of the mixin
        else:
            exprs.append(expression)

    # Set the name of the mixin
    try:
        name = states.evaluate(name_expr)
        if not name:
            raise MissingMixinName(name_expr.report)
    except TypeError:
        raise MissingMixinName(element.report)

    # Create mixin wrapper
    @states.scope
    def eval_mixin(_element,
                   _states):
        # Set xargs as variables
        for xarg, default in xargs.items():
            _states.add_element(xarg, _eval_var([default]))

        # Set args as variables
        not_defined_args  = list(args)
        not_defined_xargs = set(xargs.keys())

        try:
            for expression in _element:
                # If keyword argument
                if isinstance(expression, Attribute):
                    if expression.value in not_defined_args:
                        not_defined_args.remove(expression.value)
                        _states.add_element(
                            expression.value,
                            _eval_var([_states.evaluate(_get_value(expression))]))
                    elif expression.value in not_defined_xargs:
                        not_defined_xargs.remove(expression.value)
                        _states.add_element(
                            expression.value,
                            _eval_var([_states.evaluate(_get_value(expression))]))
                    else:
                        raise ValueError
                # If positional argument
                else:
                    _states.add_element(
                        not_defined_args.pop(0),
                        _eval_var([_states.evaluate(_get_value(expression))]))
        except (IndexError,
                KeyError,
                ValueError):
            if (expression.value in args or
                expression.value in xargs):
                    raise MixinArgumentAlreadyDefined(expression.report)
            raise UnknownMixinArgument(expression.report)

        # If some of the arguments are not defined
        if not_defined_args:
            raise TooFewExpressionsForElement(_element.report)

        # Execute mixin
        for expr in exprs:
            result = _states.evaluate(expr)
        return result

    # Register mixin in current scope
    states.add_element(name, eval_mixin)



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    '$define'     : define,
    '$undefine'   : undefine,
    '$expose'     : expose,
    #  '$is-defined' : is_defined,
    '$var'        : var,
    '$mixin'      : mixin,
    #  '?'           : branch,
    #  '$switch'     : switch
    #  '$for'        : for_,
    #  '$while'      : while_
}
