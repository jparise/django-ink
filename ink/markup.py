from docutils import nodes
from docutils.parsers.rst import directives
try:
    import pygments
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.html import _get_ttype_class
except ImportError:
    pass

class DocutilsInterface(object):
    """Parse `code` string and yield "classified" tokens.
    
    Arguments
    
      code     -- string of source code to parse
      language -- formal language the code is written in.
    
    Merge subsequent tokens of the same token-type. 
    
    Yields the tokens as ``(ttype_class, value)`` tuples, 
    where ttype_class is taken from pygments.token.STANDARD_TYPES and 
    corresponds to the class argument used in pygments html output.
    """

    def __init__(self, code, language):
        self.code = code
        self.language = language
        
    def lex(self):
        # Get lexer for language (use text as fallback)
        try:
            lexer = get_lexer_by_name(self.language)
        except ValueError:
            # info: "no pygments lexer for %s, using 'text'"%self.language
            lexer = get_lexer_by_name('text')
        return pygments.lex(self.code, lexer)
        
            
    def join(self, tokens):
        """join subsequent tokens of same token-type
        """
        tokens = iter(tokens)
        (lasttype, lastval) = tokens.next()
        for ttype, value in tokens:
            if ttype is lasttype:
                lastval += value
            else:
                yield(lasttype, lastval)
                (lasttype, lastval) = (ttype, value)
        yield(lasttype, lastval)

    def __iter__(self):
        """parse code string and yield "clasified" tokens
        """
        try:
            tokens = self.lex()
        except IOError:
            print "INFO: Pygments lexer not found, using fallback"
            # TODO: write message to INFO 
            yield ('', self.code)
            return

        for ttype, value in self.join(tokens):
            yield (_get_ttype_class(ttype), value)

def code_block_directive(name, arguments, options, content, lineno,
                         content_offset, block_text, state, state_machine):
    """Directive that parses and classifies the conents of a code_block."""
    language = arguments[0]

    # Create a literal block element and set the class argument.
    code_block = nodes.literal_block(classes=["code-block", language])

    # Parse the content with pygments and add to our code_block element.
    for cls, value in DocutilsInterface(u'\n'.join(content), language):
            code_block += nodes.inline(value, value, classes=[cls])

    return [code_block]

# Register the code_block directive.
code_block_directive.arguments = (1, 0, 1)
code_block_directive.content = 1
directives.register_directive('code-block', code_block_directive)

def render(text):
    """Renders a block of text using Docutils."""
    from docutils.core import publish_parts
    parts = publish_parts(source=text, writer_name='html4css1')
    return parts['fragment']
