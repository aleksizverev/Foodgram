from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag
def url_replace(request, field, value):
    params = request.GET.copy()
    params[field] = value
    return params.urlencode()
