## INFO ##
## INFO ##

# Import templang modules
from interpreter import interpret
from error       import TempLangError


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    input_path  = '../samples/08a.tl'
    output_path = '/tmp/tl.out'
    with open(input_path)       as input, \
         open(output_path, 'w') as output:
            try:
                interpret(input_path, input, output)
            except TempLangError as error:
                print(repr(error))
