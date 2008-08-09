import datetime
from django import template
from ink.models import Entry

register = template.Library()

class LatestEntriesNode(template.Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        entries = Entry.public.filter(pub_date__lte=datetime.datetime.now())
        context[self.varname] = list(entries[:self.num])
        return ''

@register.tag
def get_latest_entries(parser, token):
    """
    This will return a specific number of entries as the requested variable
    name.

    Usage::

        {% get_latest_entries 2 as latest %}
    """
    try:
        tag, num, _as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag takes three arguments" % token.contents.split()[0]

    if _as != 'as':
        raise template.TemplateSyntaxError, \
            "Second argument to %r tag must be 'as'" % tag

    return LatestEntriesNode(num, varname)
