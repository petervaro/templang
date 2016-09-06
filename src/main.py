## INFO ##
## INFO ##

# Import templang modules
from interpreter import interpret
from error       import TempLangError


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    with open('../samples/05.tl') as input, \
         open('/tmp/tl.out', 'w') as output:
            try:
                interpret(input, output)
            except TempLangError as error:
                print(repr(error))
