from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TagForms
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
    return render(request, "centralizer/company_list.html", {"company_list": Company.objects.all()})

def company_details(request, slug):
    comp = get_object_or_404(Company, company_slug__iexact = slug)
    return render(request, "centralizer/company_det.html", {"company": comp})

def create_tag(request):
    #check if request is 'POST'
    if request.method == 'POST':
        #bind data with form
        theform = TagForms(request.POST)    
        #if the data is valid:
        if theform.is_valid():
            #create new object with data
            tag_create = theform.save()
            #show webpage for new object
            return redirect(tag_create) # redirect knows of the get_abbsolute_url method from the model, so it needs either 1 an URL path
            # 2 The name of an URL pattern or 3 A model object with the get_absolute_url method implemented
        #else: (empty or invalid data)
        else:
            altform = TagForms()
            return render(request, 'centralizer/tagform.html', {'form': altform})
            #show bound html form with errors
            # request.method != 'POST'
            #show unbound HTML form
            
class CreateTag(View):
    theform = TagForms
    template = 'centralizer/tagform.html'
    
        