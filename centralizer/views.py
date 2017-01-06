from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
#we are already in centralizer, so we don't need call centralizer.models
from .models import Tag

def home(request):
    tags = Tag.objects.all()
    response = "<br />".join([tag.tagname for tag in tags])
    return HttpResponse(response)
