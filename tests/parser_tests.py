## INFO ##
## INFO ##

# Import python modules
from sys import path
path.insert(1, '../src')

# Import templang modules
from parser import parse
from error  import TempLangError

# TODO: Compare expected output to produced output
for i in range(1, 6):
    path = '../samples/{:>02}.tl'.format(i)
    with open(path) as file:
        try:
            print(parse(path, file.read()))
        except TempLangError as error:
            print(repr(error))
