## INFO ##
## INFO ##

ESCAPE_SEQUENCES = r'n|a|b|f|n|r|t|v|\\|0'

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
            'begin': r'\(\s*'
                    r'('
                        # Macros
                        r'('
                            r'\$('
                                r'\\(\(|\)|' + ESCAPE_SEQUENCES + r')'
                                r'|'
                                r'[^\s()]'
                            r')*'
                        r')'
                    r'|'
                        # Constants
                        r'('
                            r'[A-Z0-9-_]+'
                        r')'
                    r'|'
                        # Regulars
                        r'('
                            r'('
                                r'\\(\(|\)|' + ESCAPE_SEQUENCES + r')'
                                r'|'
                                r'[^\s()]'
                            r')*'
                        r')'
                    r')\s*',
            'beginCaptures':
            {
                2: {'name': 'entity.other.macro.{SCOPE}'},
                5: {'name': 'constant.language.{SCOPE}'},
                6: {'name': 'support.function.name.{SCOPE}'}
            },
            'patterns':
            [
                {'include' : '$self'}
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
        'comment':
        {
            'name' : 'comment.block.{SCOPE}',
            'begin': r'\(\*',
            'end'  : r'\*\)'
        },

        'attributes':
        {
            'name' : 'meta.attributes.{SCOPE}',
            'begin': r'\[\s*',
            'patterns':
            [
                {
                    'include' : '#comment'
                },
                {
                    'name' : 'variable.language.attributes.{SCOPE}',
                    'begin': r'('
                                # Internals
                                r'('
                                    r'\$('
                                        r'\\(\[|\]|' + ESCAPE_SEQUENCES + r')'
                                        r'|'
                                        r'[^\s\[\]]'
                                    r')*'
                                r')'
                            r'|'
                                # Regulars
                                r'('
                                    r'('
                                        r'\\(\[|\]|' + ESCAPE_SEQUENCES + r')'
                                        r'|'
                                        r'[^\s\[\]]'
                                    r')*'
                                r')'
                            r')\s*',
                    'beginCaptures':
                    {
                        2: {'name': 'support.type.special.{SCOPE}'},
                        5: {'name': 'storage.modifier.variable.attribute.{SCOPE}'}
                    },
                    'pattern':
                    [
                        {
                            'include' : '#comment'
                        },
                        {
                            'name'  : 'variable.language.attributes.escaped.{SCOPE}',
                            'match' : r'\\(\[|\]|' + ESCAPE_SEQUENCES + r')'
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

        #  'attributes':
        #  {
        #      'name' : 'meta.attributes.{SCOPE}',
        #      'begin': r'\[\s*'
        #          r'('
        #              # Internals
        #              r'('
        #                  r'\$('
        #                      r'\\(\[|\]|' + ESCAPE_SEQUENCES + r')'
        #                      r'|'
        #                      r'[^\s\[\]]'
        #                  r')*'
        #              r')'
        #          r'|'
        #              # Regulars
        #              r'('
        #                  r'('
        #                      r'\\(\[|\]|' + ESCAPE_SEQUENCES + r')'
        #                      r'|'
        #                      r'[^\s\[\]]'
        #                  r')*'
        #              r')'
        #          r')\s*',
        #      'beginCaptures':
        #      {
        #          2: {'name': 'support.type.special.{SCOPE}'},
        #          5: {'name': 'storage.modifier.variable.attribute.{SCOPE}'}
        #      },
        #      'patterns':
        #      [
        #          {
        #              'include' : '#comment'
        #          },
        #          {
        #              'name'  : 'string.interpolated.symbol.{SCOPE}',
        #              'match' : r'\\(\[|\]|' + ESCAPE_SEQUENCES + r')'
        #          },
        #          {
        #              'name'  : 'invalid.illegal.symbol.{SCOPE}',
        #              'match' : r'\['
        #          },
        #          {
        #              'name'  : 'variable.language.attributes.{SCOPE}',
        #              'match' : r'(?=\])|.'
        #          }
        #      ],
        #      'end' : r'\]'
        #  },

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
