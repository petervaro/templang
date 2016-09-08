## INFO ##
## INFO ##

ESCAPE_SEQUENCES = r'n|f|n|r|t|v|\\|0'

# Syntax Definition
syntax = {
    'name': '{NAME}',
    'comment': '\n\t\tWritten by Peter Varo (c)2016'
               '\n\t\thttp://github.com/petervaro/templang\n\t',
    'scopeName': 'source.{SCOPE}',
    'fileTypes': ['tl'],
    'keyEquivalent': '^~T',
    # Folding marks for the TextEditor
    'foldingStartMarker': r'\.*\(',
    'foldingStopMarker' : r'\.*\)',
    # Patterns
    'patterns':
    [
#-- COMMENT -------------------------------------------------------------------#
        {'include' : '#comment'},

#-- ELEMENTS ------------------------------------------------------------------#
        {
            'name' : 'meta.element.{SCOPE}',
            'begin': r'\(',
            'patterns':
            [
                {
                    'include' : '#whitespace'
                },
                {
                    'include' : '#comment'
                },
                {
                    'name' : 'meta.element.name.{SCOPE}',
                    'begin': r'('
                                # Macros
                                r'(\$[^\s(){}\[\]]*)'
                             r'|'
                                # Constants
                                r'([A-Z0-9-_]+)'
                             r'|'
                                # Regulars
                                r'([^\s(){}\[\]]*)'
                             r')',

                    'beginCaptures':
                    {
                        2: {'name': 'storage.modifier.variable.{SCOPE}'},
                        3: {'name': 'constant.language.{SCOPE}'},
                        4: {'name': 'support.function.name.{SCOPE}'}
                    },
                    'patterns':
                    [
                        {
                            'include' : '#whitespace'
                        },
                        {
                            'include' : '$self'
                        }
                    ],
                    'end': r'(?=\))'
                }
            ],
            'end' : r'\)'
        },

#-- ROOT ATTRIBUTES -----------------------------------------------------------#
        {
            'include' : '#attributes'
        },

#-- ROOT LITERALS -------------------------------------------------------------#
        {
            'include' : '#literals'
        },

#-- INVALIDS ------------------------------------------------------------------#
        {
            'name'  : 'invalid.illegal.text.{SCOPE}',
            'match' : r'\S+'
        }
    ],

#-- REPOSITORY ----------------------------------------------------------------#
    'repository':
    {
        'whitespace':
        {
            'name' : 'meta.whitespace.{SCOPE}',
            'match': r'\s',
        },

        'comment':
        {
            'name' : 'comment.block.{SCOPE}',
            'begin': r'\(\*',
            'patterns':
            [
                {'include': '#comment'}
            ],
            'end'  : r'\*\)'
        },

        'attributes':
        {
            'name' : 'meta.attribute.{SCOPE}',
            'begin': r'\[',
            'patterns':
            [
                {
                    'include' : '#whitespace'
                },
                {
                    'include' : '#comment'
                },
                {
                    'name' : 'meta.attribute.name.{SCOPE}',
                    'begin': r'('
                                # Internals
                                r'(\$([^\s{}\[\]](?!\(\*))*)'
                            r'|'
                                # Regulars
                                r'(((?!\(\*)[^\s{}\[\]](?!\(\*))*)'
                                #  r'(([^\s{}\[\]](?!\(\*))*)'
                            r')',
                    'beginCaptures':
                    {
                        2: {'name': 'support.type.special.{SCOPE}'},
                        4: {'name': 'variable.language.{SCOPE}'}
                    },
                    'patterns':
                    [
                        {
                            'include' : '#whitespace'
                        },
                        {
                            'include' : '#comment'
                        },
                        {
                            'include' : '#literals'
                        },
                        {
                            'name'  : 'invalid.illegal.symbol.{SCOPE}',
                            'match' : r'\['
                        }
                    ],
                    'end' : r'(?=\])'
                }
            ],
            'end' : r'\]'
        },

        'literals':
        {
            'name'  : 'meta.string.quote_braces.{SCOPE}',
            'begin': r'{',
            'patterns':
            [
                {
                    'name' : 'string.quoted.single.literal.{SCOPE}',
                    'begin': r'(?<={)',
                    'patterns':
                    [
                        {
                            'name'  : 'constant.character.escaped.{SCOPE}',
                            'match' : r'\\({|}|' + ESCAPE_SEQUENCES + r')'
                        },
                        {
                            'name'  : 'invalid.illegal.symbol.{SCOPE}',
                            'match' : r'{'
                        },
                    ],
                    'end'  : r'(?=})'
                }
            ],
            'end'  : r'}'
        },
    },
    'uuid': '2A76B6DB-0CDE-4CE9-9D95-BB415D3EF755'
}
