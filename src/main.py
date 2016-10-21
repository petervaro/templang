## INFO ##
## INFO ##

# Import python modules
from os.path   import join
from os        import mkdir
from itertools import zip_longest

# Import templang modules
from interpreter import interpret
from error       import TempLangError

#------------------------------------------------------------------------------#
EXPECT = 'Expected: {!r}, but got: {!r}'
IPATH  = '../samples'
OPATH  = '/tmp/tl'
TESTS  = []


#------------------------------------------------------------------------------#
class TestFailed(Exception): pass

#------------------------------------------------------------------------------#
class Stream:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        self._buffer = ''


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iter__(self):
        yield from (line for line in self._buffer.split('\n'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __repr__(self):
        return self._buffer


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def write(self, string):
        self._buffer += string



#------------------------------------------------------------------------------#
def test_error(error):
    if error is not None:
        raise TestFailed



#------------------------------------------------------------------------------#
def test_printed(stream, expectations):
    for printed, expected in zip_longest(stream, expectations):
        if printed != expected:
            print(EXPECT.format(expected, printed))
            raise TestFailed



#------------------------------------------------------------------------------#
def test_written(output, expectations):
    output.seek(0)
    for written, expected in zip_longest(output.read().split('\n'), expectations):
        if written != expected:
            print(EXPECT.format(expected, written))
            raise TestFailed



#------------------------------------------------------------------------------#
def ini():
    return '04.tl', '04.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(_,
        stream,
        error):
    if (error is None and
        repr(stream) != 'hello world\n'):
            raise TestFailed

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
def ini():
    return '05.tl', '05.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(output,
        stream,
        error):
    test_error(error)
    test_printed(stream,
                 ('first line',
                  'second line',
                  'third line',
                  'fourth line',
                  'first line; second line; third line; fourth line',
                  '',
                  '(alpha (beta (gamma [delta {epsilon}])))',
                  '[path {../file}]',
                  'attribute => [my-attribute] ',
                  'element => (my-element)',
                  '-----',
                  'first = alpha;',
                  'third = gamma;',
                  'second = beta;',
                  '-----',
                  'first = alpha;',
                  'second = beta;',
                  'third = gamma;',
                  ''))
    test_written(output, ('writing to the document!', ''))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
def ini():
    return '06.tl', '06.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(_,
        stream,
        error):
    test_error(error)
    test_printed(stream,
                 ('&var = hello world',
                  '&var = 12',
                  'I am printing!',
                  '',
                  'hello world!',
                  'hello world!',
                  'hello world!',
                  'hello world!',
                  'hello, world!',
                  'hello -> world!',
                  ''))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
def ini():
    return '07.tl', '07.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(_,
        stream,
        error):
    test_error(error)
    test_printed(stream,
                 ('prefix: &',
                  'type: uint64',
                  'suffix: _t',
                  'uint64_t: 12',
                  'hello there `mixin!`',
                  "first: (&prefix) = '&', "
                      "third: (&suffix) = '!', "
                      "second: (&type) = 'uint64'",
                  'templang << hello world!',
                  ''))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
def ini():
    return '08a.tl', '08.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(output,
        stream,
        error):
    test_error(error)
    test_printed(stream, ('sweet potato', ''))
    test_written(output,
                 ('hello world!',
                  '(* INFO **',
                  '** INFO *)',
                  '',
                  '[use {io}]',
                  '[use {logic}]',
                  '',
                  '($define {STRING2} {potato})',
                  '($print ($expose {STRING1}) [end { }])',
                  '',
                  '($write {world!})',
                  ''))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
def ini():
    return '09.tl', '09.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(output,
        stream,
        error):
    test_error(error)
    test_printed(stream,
                 ('<h1>Hello</h1>',
                  '<p><em>world!</em></p>',
                  '<h2>How exactly</h2>',
                  '<p>&ldquo;<strong>are</strong> you, on '
                      'this <code>beautiful</code> morning?&rdquo;</p>',
                  '<p>&mdash What?!</p>',
                  ''))
    test_written(output,
                 ('<h1>An h1 header</h1>',
                  '<p>Paragraphs are separated by a blank line.</p>',
                  '<p>2nd paragraph. <em>Italic</em>, <strong>bold</strong>, '
                     'and <code>monospace</code>. Itemized lists',
                  'look like:</p>',
                  '<ul>',
                  '<li>this one</li>',
                  '<li>that one</li>',
                  '<li>the other one</li>',
                  '</ul>',
                  '<p>Note that &mdash; not considering the '
                     'asterisk &mdash; the actual text',
                  'content starts at 4-columns in.</p>',
                  '<blockquote>',
                  '<p>Block quotes are',
                  'written like so.</p>',
                  '<p>They can span multiple paragraphs,',
                  'if you like.</p>',
                  '</blockquote>',
                  '<p>Use 3 dashes for an em-dash. Use 2 dashes for '
                     'ranges (ex., &ldquo;it&rsquo;s all',
                  'in chapters 12&mdash14&rdquo;). Three dots &hellip; '
                     'will be converted to an ellipsis.',
                  'Unicode is supported.</p>'))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#  #------------------------------------------------------------------------------#
#  def ini():
#      return '11a.tl', '11.out', Stream()

#  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#  def fin(output,
#          _,
#          error):
#      print()
#      #  test_error(error)
#      #  test_printed(stream,
#      #               ())
#      #  test_written(output,
#      #               ())

#  #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
#  TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
def ini():
    return '13.tl', '13.out', Stream()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fin(output,
        _,
        error):
    test_error(error)
    test_written(output, ('<custom-tag class="xyz"></custom-tag>',))

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
TESTS.append({'ini': ini, 'fin': fin})



#------------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        mkdir(OPATH)
    except FileExistsError:
        pass

    for i, test in enumerate(TESTS, start=1):
        error = None
        ipath, opath, stream = test['ini']()
        ipath = join(IPATH, ipath)
        opath = join(OPATH, opath)
        print('[{}] RUNNING TEST: `{}`'.format(i, ipath))
        with open(ipath) as src, open(opath, 'w+') as dst:
            try:
                interpret(ipath, src, dst, stream)
            except TempLangError as exception:
                error = exception
                print(repr(exception))

            try:
                test['fin'](dst, stream, error)
                print('[{}] TEST FINISHED: SUCCESS\n'.format(i))
            except TestFailed:
                print('[{}] TEST FINISHED: FAILURE\n'.format(i))
