## INFO ##
## INFO ##

# Import python modules
from itertools import chain, islice

WHITE_SPACES      = ' \t\v'
ATTRIBUTE_ESCAPES = {
    '\\' : '\\',
    '['  : '[',
    ']'  : ']'
}
LITERAL_ESCAPES   = {
    '\\' : '\\',
    '{'  : '{',
    '}'  : '}',
    'n'  : '\n',
    't'  : '\t',
    'v'  : '\v',
    '0'  : '\x00'
}

#------------------------------------------------------------------------------#
class Expression:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, report):
        self._value = ''
        self.report = report


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iadd__(self, value):
        self._value += value
        return self



#------------------------------------------------------------------------------#
class Element(Expression):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_name_finished = False
        self._children         = []


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iadd__(self, value):
        # If the given value is a white-space character
        if value in WHITE_SPACES:
            # If element already has a name
            if self._value:
                self._is_name_finished = True
        # If this element already have a name
        elif self._is_name_finished:
            raise UnexpectedCharacter
        # If the given character should be added to the element's name
        else:
            self._value += value
        return self


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        if self._children:
            return ('<Element name="{}">{}'
                    '</Element>').format(self._value,
                                         ''.join(map(str, self._children)))
        else:
            return '<Element name="{}"/>'.format(self._value)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def append(self, child):
        self._is_name_finished = True
        self._children.append(child)



#------------------------------------------------------------------------------#
class Attribute(Expression):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        if self._value:
            return '<Attribute>{}</Attribute>'.format(self._value)
        else:
            return '<Attribute/>'



#------------------------------------------------------------------------------#
class Literal(Expression):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        if self._value:
            return '<Literal>{}</Literal>'.format(self._value)
        else:
            return '<Literal/>'



#------------------------------------------------------------------------------#
class Root(Element):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, *args, **kwargs):
        super().__init__(report=None, *args, **kwargs)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return '<Root>{}</Root>'.format(''.join(map(str, self._children)))




#------------------------------------------------------------------------------#
class CommentIsNotOpen(Exception): pass


#------------------------------------------------------------------------------#
class ParseStatesReport:

    @property
    def line(self):
        return self._lines[self._line_index]

    @property
    def line_index(self):
        return self._line_index

    @property
    def char_index(self):
        return self._char_index


    def __init__(self, lines,
                       line_index,
                       char_index):
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
        line_index = self._line_index if line_index is None else line_index
        char_index = self._char_index if char_index is None else char_index
        return ParseStatesReport(self._lines, line_index, char_index)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, lines):
        self._line_index    = 0
        self._char_index    = 0
        self._comment_level = 0
        self._stored_state  = None
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
            for self._curr_char in line:
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
class SyntacticError(Exception):

    MESSAGE       = ''
    NOTE          = ''
    FORMAT_STRING = ('\n'
                     'Error: {ERROR.MESSAGE}\n'
                     'In line {LINENO}, at column {COLUMN}:\n\n'
                     '    {LINE}\n'
                     '    {PADDING}^\n'
                     '{ERROR.note}')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, report=None):
        self._report = report
        self.note    = '(Note: {})\n'.format(self.NOTE) if self.NOTE else ''


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        report = self._report
        return self.FORMAT_STRING.format(ERROR   = self,
                                         LINE    = report.line,
                                         LINENO  = report.line_index + 1,
                                         COLUMN  = report.char_index + 1,
                                         PADDING = report.char_index*' ')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class InvalidEscapeSequence(SyntacticError):
    MESSAGE = "Invalid escape sequence found"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedCharacter(SyntacticError):
    MESSAGE = "Unexpected character found"
    NOTE    = "At this level only elements, attributes and literals are allowed"
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
    NOTE    = "Brackets can be used inside attributes by escaping them: `\\[`"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
class UnexpectedLiteralOpening(UnexpectedCharacter):
    MESSAGE = "Unexpected character found: `{`"
    NOTE    = "Braces can be used inside literals by escaping them: `\\{`"



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

        print('comment level:', states.is_comment_open)
        _debug(states)

        if literal:
            if char == '\\':
                char = next(states)
                char = LITERAL_ESCAPES.get(char, '\\' + char)

            elif char == '}':
                try:
                    element.append(literal)
                except AttributeError as e:
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
            if char == '\\':
                char = next(states)
                char = ATTRIBUTE_ESCAPES.get(char, '\\' + char)

            elif (char == '(' and
                  states.next_char == '*'):
                    next(states)
                    states.comment_open()
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

            attribute += char

        elif element:
            if char == '(':
                if states.next_char == '*':
                    next(states)
                    states.comment_open()
                    continue

                print('> elem')
                states.step_back()
                try:
                    _parse(element, states)
                except UnbalancedClosingParenthesis:
                    states.step_back()
                print('< elem')
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

            element += char
            continue

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
def parse(text: str):
    if not isinstance(text, str):
        raise ValueError('first argument should be `str` and not:',
                         text.__class__.__qualname__)

    return _parse(root   = Root(),
                  states = ParseStates(text.split('\n')))
