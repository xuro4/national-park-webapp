from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_add(context, field, value):
    dict_ = context['request'].GET.copy()
    dict_[field] = str(int(context['page']) + value)
    return dict_.urlencode()


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    dict_ = context['request'].GET.copy()
    dict_[field] = value
    return dict_.urlencode()