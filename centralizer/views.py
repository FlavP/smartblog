from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template import Context, loader
# Create your views here.
#we are already in centralizer, so we don't need call centralizer.models
from .models import Tag

def home(request):
    tags = Tag.objects.all()
    #Rewrite 7 times
    template = loader.get_template('centralizer/taglist.html')
    context = Context({'taglist':tags})
    response = template.render(context)
    return HttpResponse(response)

def tagdetails(request, slug):
    try:
        tag = Tag.objects.get(tag_slug__iexact=slug)
    except Tag.DoesNotExist:
        raise Http404
    template = loader.get_template('centralizer/tagdetails.html')
    context = Context({'thetag':tag})
    return HttpResponse()