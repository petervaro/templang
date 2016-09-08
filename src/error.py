## INFO ##
## INFO ##

#------------------------------------------------------------------------------#
class TempLangError(Exception):

    MESSAGE       = ''
    NOTE          = ''
    FORMAT_STRING = ('\n'
                     'Error: {ERROR.MESSAGE}\n'
                     'In file "{PATH}", line {LINENO}, column {COLUMN}:\n\n'
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
                                         PATH    = report.path,
                                         LINE    = report.line,
                                         LINENO  = report.line_index + 1,
                                         COLUMN  = report.char_index + 1,
                                         PADDING = report.char_index*' ')
