## INFO ##
## INFO ##

#------------------------------------------------------------------------------#
def python(element,
           states):
    try:
        source, *_ = element
        exec(source.value)
    except ValueError:
        pass


#------------------------------------------------------------------------------#
# Export keywords
ELEM_KEYWORDS = {
    '>>>' : python
}
