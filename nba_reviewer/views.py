from django.http import  HttpResponse
from django.template import RequestContext, loader

def about(request):
    template = loader.get_template('about/about.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def contact(request):
    template = loader.get_template('contact/contact.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))