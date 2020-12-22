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


@register.filter
def get_filter_values(element):
    return element.getlist('filters')


@register.filter
def get_filtered_tags(request, tag):
    new_request = request.GET.copy()
    if tag.slug in request.GET.getlist('filters'):

        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)

    else:
        new_request.appendlist('filters', tag.slug)
    return new_request.urlencode()
