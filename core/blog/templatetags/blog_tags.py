from django.template import Library

register = Library()

# this tag will return queries in url of page except page query.
@register.simple_tag(name="queries")
def otherqueries(request):
    str = ""
    for key,value in request.GET.items():
          if key != 'page':
             str =  str  + key + "=" + value + "&"
    return str
