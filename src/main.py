## INFO ##
## INFO ##

# Import templang modules
from parser import parse, SyntacticError


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    with open('../samples/02.tl') as file:
        try:
            print(parse(file.read()))
        except SyntacticError as exception:
            print(repr(exception))
