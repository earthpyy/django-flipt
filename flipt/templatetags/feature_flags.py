"""
Usage:
{% featureflag <flag_key> [<flag_state=True>] %}
    ...
{% endfeatureflag %}
"""
from django import template

from flipt.flags import flag_enabled

register = template.Library()


@register.tag
def featureflag(parser, token):
    nodelist = parser.parse(('endfeatureflag',))
    parser.delete_first_token()

    try:
        _, params = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires one or two arguments' % token.contents.split()[0]
        ) from ValueError

    params = params.split()
    flag_key = str(params[0]).rstrip('"').lstrip('"')
    state = params[1] if len(params) > 1 else True

    return FeatureFlagNode(nodelist, flag_key, state)


class FeatureFlagNode(template.Node):
    def __init__(self, nodelist, flag_key: str, state: bool):
        self.nodelist = nodelist
        self.flag_key = flag_key
        self.state = state

    def render(self, context):
        should_render = self.state == flag_enabled(self.flag_key)
        return self.nodelist.render(context) if should_render else ''
