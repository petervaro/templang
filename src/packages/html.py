## INFO ##
## INFO ##

# Import python modules
from itertools import chain, zip_longest

# Import beautifulsoup modules

# Import markdown modules
from markdown import markdown

# Import templang modules
from parser      import Attribute
from interpreter import (UnknownAttributeForElement,
                         ElementParameterTypeError)


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
        (!-- <ANYTHING>)
    """
    contents = '<!-- '
    for expression in element:
        content = states.evaluate(expression)
        if isinstance(content, str):
            content = str(content)
        contents += content
    return contents + ' -->'



#------------------------------------------------------------------------------#
def tag(element,
        states):
    """
    Usage:
        (<TAG> [<PROPERTY1> <VALUE1> <VALUE2> <VALUE...>]
               [<PROPERTY2> <VALUE1> <VALUE2> <VALUE...>]
               [<PROPERTY...> <VALUE1> <VALUE2> <VALUE...>]
               [$join <SEPARATOR>]
               [$split <SEPARATOR>]
               [$return]
               [$custom])

    $join   : join literals with SEPARATOR
    $split  : split literals at SEPARATOR
    $return : return string instead of writing to output
    $custom : tag is not an HTML5 one
    """
    #  contents = ''




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
