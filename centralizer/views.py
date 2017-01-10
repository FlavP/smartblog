from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render
# Create your views here.
#we are already in centralizer, so we don't need call centralizer.models
from .models import Tag, Company

def taglist(request):
    return render(request, "centralizer/taglist.html",
                  {"taglist":Tag.objects.all()})

def tagdetails(request, slug):
    tag = get_object_or_404(Tag, tag_slug__iexact = slug)
    return render(request, "centralizer/tagdetails.html",
                  {"tag": tag})

def companies(request):
    return render(request, "centralizer/company_list.html", {"company": Company.objects.all()})

def company_details(request, slug):
    comp = get_object_or_404(Company, company_slug__iexact = slug)
    return render(request, "centralizer/company_det.html", {"company": comp})