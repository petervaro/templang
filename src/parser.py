## INFO ##
## INFO ##

# Import python modules
from itertools import chain, islice

# Import templang modules
from error import TempLangError


#------------------------------------------------------------------------------#
# Module level constants
WHITE_SPACES      = ' \t\v\n'
LITERAL_ESCAPES   = {
    '\\' : '\\',
    '\n' : '',
    '{'  : '{',
    '}'  : '}',
    'n'  : '\n',
    't'  : '\t',
    'r'  : '\r',
    'f'  : '\f',
    'v'  : '\v',
    '0'  : '\x00'
}



#------------------------------------------------------------------------------#
class Expression:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self._value = value


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, report):
        self._value = ''
        self.report = report


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iadd__(self, value):
        self._value += value
        return self



#------------------------------------------------------------------------------#
class Container(Expression):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_name_finished = False
        self._children         = []


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iadd__(self, value):
        # If the given value is a white-space character
        if value in WHITE_SPACES:
            # If container already has a name
            if self._value:
                self._is_name_finished = True
        # If this container already have a name
        elif self._is_name_finished:
            raise UnexpectedCharacter
        # If the given character should be added to the container's name
        else:
            self._value += value
        return self


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iter__(self):
        yield from self._children


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def append(self, child):
        self._is_name_finished = True
        self._children.append(child)



#------------------------------------------------------------------------------#
class Element(Container):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        if self._children:
            if self._value:
                return '({} {})'.format(self._value,
                                        ' '.join(map(str, self._children)))
            return '({})'.format(' '.join(map(str, self._children)))
        return '({})'.format(self._value)



#------------------------------------------------------------------------------#
class Attribute(Container):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        if self._children:
            if self._value:
                return '[{} {}]'.format(self._value,
                                        ' '.join(map(str, self._children)))
            return '[{}]'.format(' '.join(map(str, self._children)))
        return '[{}]'.format(' '.join(self._value.strip().split()))



#------------------------------------------------------------------------------#
class Literal(Expression):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return '{{{}}}'.format(self._value)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iadd__(self, value):
        self._value += value
        return self



#------------------------------------------------------------------------------#
class Root(Element):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, *args, **kwargs):
        super().__init__(report=None, *args, **kwargs)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return ' '.join(map(str, self._children))




#------------------------------------------------------------------------------#
class CommentIsNotOpen(Exception): pass


#------------------------------------------------------------------------------#
class ParseStatesReport:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def path(self):
        return self._path

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def line(self):
        return self._lines[self._line_index]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def line_index(self):
        return self._line_index

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def char_index(self):
        return self._char_index


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, path,
                       lines,
                       line_index,
                       char_index):
        self._path       = path
        self._lines      = lines
        self._line_index = line_index
        self._char_index = char_index



#------------------------------------------------------------------------------#
class ParseStates:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def line(self):
        return self._lines[self._line_index]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def line_index(self):
        return self._line_index

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def char_index(self):
        return self._char_index

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def is_comment_open(self):
        return self._comment_level

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def curr_char(self):
        return self._curr_char


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def next_char(self):
        # If cursor is not at the last character of current line
        try:
            # Get next character of current line
            return self._lines[self._line_index][self._char_index + 1]
        # If cursor is at the last character of the current line
        except IndexError:
            # Get first character of next line
            return self._lines[self._line_index + 1][0]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def prev_char(self):
        # If cursor is not at the first character in the current line
        if self._char_index:
            # Get previous character of current line
            return self._lines[self._line_index][self._char_index - 1]
        # If cursor is at the first character in the current line
        else:
            # TODO: what about `...*\n)` -- will this be a comment?
            # Get last character of previous line
            return self._lines[self._line_index - 1][-1]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def report(self, line_index=None,
                     char_index=None):
        return ParseStatesReport(
            self._path,
            self._lines,
            self._line_index if line_index is None else line_index,
            self._char_index if char_index is None else char_index)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, path,
                       lines):
        self._line_index    = 0
        self._char_index    = 0
        self._comment_level = 0
        self._stored_state  = None
        self._path          = path
        self._lines         = lines
        self._iter_chars    = self._new_iter_chars()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iter__(self):
        return self


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __next__(self):
        return next(self._iter_chars)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def _new_iter_chars(self, line_index=0,
                              char_index=0):
        # Create a slice of lines based on the provided indices
        lines = chain((islice(self._lines[line_index], char_index, None),),
                      islice(self._lines, line_index + 1, None))

        self._char_index = char_index
        # Iterate over the sliced lines, update line index
        for self._line_index, line in enumerate(lines, line_index):
            # Iterate over the current line
            for self._curr_char in chain(line, '\n'):
                yield self._curr_char
                # Update column index
                self._char_index += 1
            self._char_index = 0

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def step_back(self):
        # Stepping back means, repeating the already consumed last character
        self._iter_chars = self._new_iter_chars(self._line_index,
                                                self._char_index)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def comment_open(self):
        self._comment_level += 1


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def comment_close(self):
        if self._comment_level:
            self._comment_level -= 1
        else:
            raise CommentIsNotOpen



#------------------------------------------------------------------------------#
class SyntacticError(TempLangError): pass
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidEscapeSequence(SyntacticError):
    MESSAGE = "Invalid escape sequence found"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedCharacter(SyntacticError):
    MESSAGE = "Unexpected character found"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedOpeningParenthesis(SyntacticError):
    MESSAGE = "Unbalanced opening parenthesis: `(`"
    NOTE    = "Missing its closing counterpart: `)`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedOpeningBracket(SyntacticError):
    MESSAGE = "Unbalanced opening bracket: `[`"
    NOTE    = "Missing its closing counterpart: `]`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedOpeningBrace(SyntacticError):
    MESSAGE = "Unbalanced opening brace: `{`"
    NOTE    = "Missing its closing counterpart: `}`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedCommentClosure(SyntacticError):
    MESSAGE = "Unbalanced comment closure sequence: `*)`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedClosingParenthesis(SyntacticError):
    MESSAGE = "Unbalanced closing parenthesis: `)`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedClosingBracket(SyntacticError):
    MESSAGE = "Unbalanced closing bracket: `]`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnbalancedClosingBrace(SyntacticError):
    MESSAGE = "Unbalanced closing brace: `}`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedAttributeOpening(UnexpectedCharacter):
    MESSAGE = "Unexpected character found: `[`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedLiteralOpening(UnexpectedCharacter):
    MESSAGE = "Unexpected character found: `{`"
    NOTE    = "Braces can be used inside literals by escaping them: `\\{`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedCharacterInElement(UnexpectedCharacter):
    NOTE = "At this level only elements, attributes and literals are allowed"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedCharacterInAttribute(UnexpectedCharacter):
    NOTE = "At this level only elements and literals are allowed"



#------------------------------------------------------------------------------#
def _debug(states):
    if states.curr_char not in WHITE_SPACES:
        print('char:'     , states.curr_char,
              'in line:'  , states.line_index + 1,
              'at column:', states.char_index + 1)



#------------------------------------------------------------------------------#
def _parse(root   : Element,
           states : ParseStates):

    # Local states
    element   = None
    attribute = None
    literal   = None

    for char in states:

        if literal:
            if char == '\\':
                char = next(states)
                char = LITERAL_ESCAPES.get(char, '\\' + char)

            elif char == '}':
                try:
                    attribute.append(literal)
                except AttributeError:
                    try:
                        element.append(literal)
                    except AttributeError:
                        root.append(literal)
                literal = None
                continue

            elif char == '{':
                raise UnexpectedLiteralOpening(states.report)

            literal += char

        elif states.is_comment_open:
            if (char == '*' and
                states.next_char == ')'):
                    try:
                        states.comment_close()
                    except CommentIsNotOpen:
                        raise UnbalancedCommentClosure(states.report)
                    next(states)

            elif (char == '(' and
                  states.next_char == '*'):
                    states.comment_open()
                    next(states)
            continue

        elif attribute:

            if char == '(':
                if states.next_char == '*':
                    next(states)
                    states.comment_open()
                    continue

                states.step_back()
                try:
                    _parse(attribute, states)
                except UnbalancedClosingBracket:
                    states.step_back()
                continue

            elif char == '{':
                literal = Literal(states.report)
                continue

            elif char == ']':
                try:
                    element.append(attribute)
                except AttributeError as e:
                    root.append(attribute)
                attribute = None
                continue

            elif char == '[':
                raise UnexpectedAttributeOpening(states.report)

            try:
                attribute += char
            except UnexpectedCharacter:
                raise UnexpectedCharacterInAttribute(states.report)


        elif element:
            if char == '(':
                if states.next_char == '*':
                    next(states)
                    states.comment_open()
                    continue

                states.step_back()
                try:
                    _parse(element, states)
                except UnbalancedClosingParenthesis:
                    states.step_back()
                continue

            elif char == ')':
                root.append(element)
                element = None
                continue

            elif char == '[':
                attribute = Attribute(states.report)
                continue

            elif char == '{':
                literal = Literal(states.report)
                continue

            try:
                element += char
            except UnexpectedCharacter:
                raise UnexpectedCharacterInElement(states.report)

        elif char == '(':
            if states.next_char == '*':
                next(states)
                states.comment_open()
            else:
                element = Element(states.report)

        elif char == ')':
            raise UnbalancedClosingParenthesis(states.report)

        elif char == '[':
            attribute = Attribute(states.report)

        elif char == ']':
            raise UnbalancedClosingBracket(states.report)

        elif char == '{':
            literal = Literal(states.report)

        elif char == '}':
            raise UnbalancedOpeningBrace(states.report)

        else:
            # If character is not a white space
            if char not in WHITE_SPACES:
                raise UnexpectedCharacter(states.report)

    # TODO: ** Unbalanced comment closure **
    #       Check if there is any comment left open. That also means, each
    #       comment level should know its own position too, just as expressions

    # Iterate through all the possible tokens at this level
    for expression, error in ((element  , UnbalancedOpeningParenthesis),
                              (attribute, UnbalancedOpeningBracket),
                              (literal  , UnbalancedOpeningBrace)):
        # If any token is still open
        if expression:
            raise error(expression.report)

    # Return constructed data structure
    return root



#------------------------------------------------------------------------------#
def parse(path: str,
          text: str):
    if not isinstance(text, str):
        raise ValueError('first argument should be `str` and not:',
                         text.__class__.__qualname__)

    return _parse(root   = Root(),
                  states = ParseStates(path, text.split('\n')))
