from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render, redirect
from .forms import TagForms, CompanyForms, NewsForm
from django.views.generic import View
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
    theformclass = TagForms
    template = 'centralizer/tagform.html'

    def get(self, request):
        return render(request, self.template, {'form': self.theformclass})
    
    def post(self, request):
        bounded_form = self.theformclass(request.POST)
        if bounded_form.is_valid():
            the_new_tag = bounded_form.save()
            return redirect(the_new_tag)
        else:
            return render(request, self.template, {'form': bounded_form})

class CreateCompany(View):
    theformclass = CompanyForms
    template = 'centralizer/compcreate.html'

    def get(self, request):
        return render(request, self.template, {'form': self.theformclass})

    def post(self, request):
        new_company = request.POST
        if new_company.is_valid:
            new_company.save()
            return redirect(new_company)
        else:
            return render(request, self.template, {'form': self.theformclass})

class CreateNews(View):
    theformclass = NewsForm
    template = 'centralizer/relnewscreate.html'

    def get(self, request):
        return render(request, self.template, {"form": self.template})

    def post(self, request):
        new_news = request.POST
        if new_news.is_valid():
            new_news.save()
            #News nu are get_absolute_url in model, dar folosim metoda din company pentru redirect,
            #  old code: redirect(new_news).company
            return redirect(new_news)
        else:
            return render(request, self.template, {"form": self.template})