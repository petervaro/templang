## INFO ##
## INFO ##

# Import python modules
from collections import OrderedDict
from itertools   import chain, zip_longest

# Import beautifulsoup modules
from bs4 import BeautifulSoup

# Import markdown modules
from markdown import markdown

# Import templang modules
from parser      import Attribute, Literal
from interpreter import (UnknownAttributeForElement,
                         ElementParameterTypeError,
                         TooFewAttributeParameter,
                         TooManyAttributeParameters)


#------------------------------------------------------------------------------#
class HTMLTag:

    def __init__(self, name):
        self.name = name
        self.attr = {}
        self.cont = []


#------------------------------------------------------------------------------#
# Module level internal constants
_MD_ARGS = {
    'output_format'     : 'html5',
    'extensions'        : ('markdown.extensions.extra',
                           'markdown.extensions.smarty',
                           'markdown.extensions.sane_lists'),
    'extension_configs' :
    {
        'markdown.extensions.smarty':
        {
            'substitutions':
            {
                'ndash' : '&mdash'
            }
        }
    }
}
_HTML_TAGS = (
    '!doctype'  , 'a'      , 'abbr'    , 'address' , 'area'      , 'article' ,
    'aside'     , 'audio'  , 'b'       , 'base'    , 'bdi'       , 'bdo'     ,
    'blockquote', 'body'   , 'br'      , 'button'  , 'canvas'    , 'caption' ,
    'cite'      , 'code'   , 'col'     , 'colgroup', 'datalist'  , 'dd'      ,
    'del'       , 'details', 'dfn'     , 'dialog'  , 'div'       , 'dl'      ,
    'dt'        , 'em'     , 'embed'   , 'fieldset', 'figcaption', 'figure'  ,
    'footer'    , 'form'   , 'h1'      , 'h2'      , 'h3'        , 'h4'      ,
    'h5'        , 'h6'     , 'head'    , 'header'  , 'hr'        , 'html'    ,
    'i'         , 'iframe' , 'img'     , 'input'   , 'ins'       , 'kbd'     ,
    'keygen'    , 'label'  , 'legend'  , 'li'      , 'link'      , 'link'    ,
    'main'      , 'map'    , 'mark'    , 'menu'    , 'menuitem'  , 'meta'    ,
    'meter'     , 'nav'    , 'noscript', 'object'  , 'ol'        , 'optgroup',
    'option'    , 'output' , 'p'       , 'param'   , 'pre'       , 'progress',
    'q'         , 'rp'     , 'rt'      , 'ruby'    , 'ruby'      , 's'       ,
    'samp'      , 'script' , 'section' , 'select'  , 'small'     , 'source'  ,
    'span'      , 'strong' , 'style'   , 'sub'     , 'summary'   , 'sup'     ,
    'table'     , 'tbody'  , 'td'      , 'textarea', 'tfoot'     , 'th'      ,
    'thead'     , 'time'   , 'title'   , 'tr'      , 'track'     , 'u'       ,
    'ul'        , 'var'    , 'video'   , 'wbr'
)



#------------------------------------------------------------------------------#
def comment(element,
            states):
    """
    Usage:
        (!-- <ANYTHING...>
             [$join <SEPARATOR>]
             [$return <OPTIONAL-CONDITION>])
    """
    # TODO: **comment should behave like a tag**
    #       Implement the $join and the $return attributes for comment
    contents = '<!-- '
    for expression in element:
        content = states.evaluate(expression)
        if not isinstance(content, str):
            content = str(content)
        contents += content
    contents += ' -->'
    states.output.write(contents)



#------------------------------------------------------------------------------#
def tag(element,
        states):
    """
    Usage:
        (<TAG> [<PROPERTY1> <VALUE1> <VALUE2> <VALUE...>]
               [<PROPERTY2> <VALUE1> <VALUE2> <VALUE...>]
               [<PROPERTY...> <VALUE1> <VALUE2> <VALUE...>]
               [$join <SEPARATOR>]
               [$return <OPTIONAL-CONDITION>]

    $join       : join literals with SEPARATOR
    $return     : return string instead of writing to output
    """

    join       = None
    return_    = False
    return_all = False
    attributes = {}
    nodes      = []
    for expression in element:
        if isinstance(expression, Attribute):
            if expression.value == '$join':
                try:
                    sep, *rest = expression
                    if rest:
                        raise TooManyAttributeParameters(rest[0].report)
                except ValueError:
                    raise TooFewAttributeParameter(expression.report)
                join = states.evaluate(sep)

            # TODO: **handle options for $return(-all)**
            #       By default both $return and $return-all should represent
            #       True values, that is, if no value is provided, their
            #       presence means teh value is True. Otherwise the first value
            #       should be treated as a boolean-expression

            elif expression.value == '$return':
                return_ = True
            elif expression.value == '$return-all':
                return_all = return_ = True
            else:
                attributes[expression.value] = ' '.join(map(states.evaluate, expression))
        else:
            nodes.append(expression)

    if return_:
        return '<{NAME} {ATTR}>{CONT}</{NAME}>'.format(
            NAME=element.value,
            ATTR=' '.join(k + '="' + v + '"' if v else k for k, v in attributes.items()),
            CONT=(join or '').join(states.evaluate(n) for n in nodes))
    else:
        states.output.write('<{} {}>'.format(
            element.value,
            ' '.join(k + '="' + v + '"' if v else k for k, v in attributes.items())))
        join = join or ''
        for i, node in enumerate(nodes):
            if isinstance(node, Literal):
                if i:
                    states.output.write(join)
                states.output.write(states.evaluate(node))
            else:
                states.evaluate(node)
        states.output.write('</{}>'.format(element.value))

    #  soup = BeautifulSoup('', 'html5lib')
    #  soup.contents = html
    #  html = soup.prettify()



#------------------------------------------------------------------------------#
def markdown_(element,
              states):
    """
    Usage:
        (markdown <VALUE1> <VALUE2> <VALUE...> [$return])

    $return : return string instead of writing to output
    """
    contents = ''
    return_  = False
    for expression in element:
        if isinstance(expression, Attribute):
            if expression.value == '$return':
                return_ = True
            else:
                raise UnknownAttributeForElement(expression.report)
        else:
            content = states.evaluate(expression)
            if not isinstance(content, str):
                raise ElementParameterTypeError(expression.report)
            contents += markdown(content, **_MD_ARGS)

    if return_:
        return contents
    states.output.write(contents)



#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    k:v for k, v in zip_longest(chain(('!--', 'markdown'), _HTML_TAGS),
                                (comment, markdown_),
                                fillvalue=tag)
}
