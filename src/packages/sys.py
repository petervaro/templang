## INFO ##
## INFO ##

# Import python modules
from subprocess import run, PIPE

# Import templang modules
from parser      import Attribute
from interpreter import (UnknownAttributeForElement,
                         ElementParameterTypeError)

#------------------------------------------------------------------------------#
def shell(element,
          states):
    """
    Usage:
        (shell <COMMAND1> <COMMAND2> <COMMAND...> [redirect])
    """
    pipe     = None
    commands = []
    for expression in element:
        if isinstance(expression, Attribute):
            # TODO: **pass boolean flag**
            #       the redirect switch should be able to receive a boolean flag
            #       so that it can be switched on or off programatically
            if expression.value == 'redirect':
                pipe = PIPE
            else:
                raise UnknownAttributeForElement(expression.report)
        else:
            command = states.evaluate(expression)
            if isinstance(command, str):
                commands.append(command)
            else:
                raise ElementParameterTypeError(expression.report)

    results = ''
    for command in commands:
        result = run(command, stderr=pipe, stdout=pipe, shell=True)
        results += result.stdout.decode('utf-8')
        results += result.stderr.decode('utf-8')

    return results



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    'shell' : shell
}
