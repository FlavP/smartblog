from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .forms import TagForms, CompanyForms, NewsForm
from django.views.generic import View
from .utils import ViewObjectsMixin, UpdateObjectsMixin, DeleteObjectMixin
from .models import RelatedNews
# Create your views here.
#we are already in centralizer, so we don't need call centralizer.models
from .models import Tag, Company
from django.urls.base import reverse_lazy

def taglist(request):
    return render(request, "centralizer/taglist.html",
                  {"taglist":Tag.objects.all()})

def tagdetails(request, slug):
    tag = get_object_or_404(Tag, tag_slug__iexact = slug)
    return render(request, "centralizer/tagdetails.html",
                  {"tag": tag})

def companies(request):
    return render(request, "centralizer/company_list.html", {"companies": Company.objects.all()})

class TagList(View):
    template = "centralizer/taglist.html"
    def get(self, request):
        tags = Tag.objects.all()
        context = {"taglist": tags}
        return render(request, self.template, context)

class PagedTag(View):
    tags_per_page = 4
    template = "centralizer/taglis.html"
    def get(self, request, page=None):
        tags = Tag.objects.all()
        pagus = Paginator(tags, self.tags_per_page)
        try:
            tagpage = pagus.page(page)
        except PageNotAnInteger:
            tagpage = pagus.page(1)
        except EmptyPage:
            tagpage = pagus.page(pagus.num_pages)
        if tagpage.has_previous():
            prev_page = reverse('centralizer_tag_page', args=(tagpage.previous_page_number()))
        else:
            prev_page = None
        if tagpage.has_next():
            next_page = reverse('centralizer_tag_page', args=(tagpage.next_page_number()))
        else:
            next_page = None
        context = {"taglist": tags, "next_page": next_page, "prev_page": prev_page, "has_pages": tagpage.has_other_pages(),
                   "pagus": pagus}
        return render(request, self.template, context)

class CompanyList(View):
    pagini = 4
    template = "centralizer/company_list.html"
    page_query = 'page'
    
    def get(self, request):
        companies = Company.objects.all()
        page_no = request.GET.get(self.page_query)
        pagin = Paginator(companies, self.pagini)
        try:
            page = pagin.page(page_no)
        except PageNotAnInteger:
            page = pagin.page(1)
        except EmptyPage:
            page = pagin.page(pagin.num_pages)
        if page.has_previous():
            previous_page = "?{prev}={n}".format(prev=self.page_query, n=page.previous_page_number())
        else:
            previous_page = None
        if page.has_next():
            next_page = "{next}={n}".format(next=self.page_query, n=page.next_page_number())
        else:
            next_page=None
        context = {'companies' : page, 'paginator': pagin,
                   "has_pages": pagin.has_other_pages(), "next_page": next_page, "previous_page": previous_page}
        return render(request, self.template, context)

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
            
class CreateTag(ViewObjectsMixin, View):
    theformclass = TagForms
    template = 'centralizer/tagform.html'
'''
The old way, without refactoring. Now we import the Object Mixin with the view and use it's methods with the form class and template defined
    def get(self, request):
        return render(request, self.template, {'form': self.theformclass})
    
    def post(self, request):
        bounded_form = self.theformclass(request.POST)
        if bounded_form.is_valid():
            the_new_tag = bounded_form.save()
            return redirect(the_new_tag)
        else:
            return render(request, self.template, {'form': bounded_form})
'''
class CreateCompany(ViewObjectsMixin, View):
    theformclass = CompanyForms
    template = 'centralizer/compcreate.html'
'''
    def get(self, request):
        return render(request, self.template, {'form': self.theformclass})

    def post(self, request):
        new_company = request.POST
        if new_company.is_valid:
            new_company.save()
            return redirect(new_company)
        else:
            return render(request, self.template, {'form': self.theformclass})
'''
    
class CreateNews(ViewObjectsMixin, View):
    theformclass = NewsForm
    template = 'centralizer/relnewscreate.html'
'''
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
            '''
class UpdateNews(View):
    theformclass = NewsForm
    template = "centralizer/relnewsup.html"

    def get_update_url(self):
        return reverse("centralizer_update_related", kwargs={'pk': self.pk})

    def get(self, request, pk):
        relnews = get_object_or_404(RelatedNews, pk=pk)
        context = {
            "theform": self.theformclass(instance=relnews),
            "relatednews": relnews
                   }
        return render(request, self.template, context)

    def post(self, request, pk):
        relnews = get_object_or_404(RelatedNews, pk=pk)
        is_valid_form = self.theformclass(request.POST, instance=relnews)
        if is_valid_form.is_valid():
            newnews = is_valid_form.save()
            return redirect(newnews)
        else:
            context = {
                "theform": self.theformclass,
                "relatednews": relnews
            }
            return render(request, self.template, context)

class DeleteNews(View):
    def get(self, request, pk):
        delnews = get_object_or_404(RelatedNews, pk = pk)
        return render(request, 'centralizer/relnewsdel.html', {'news': delnews})
    
    def post(self, request, pk):
        delnews = get_object_or_404(RelatedNews, pk = pk)
        company = delnews.company
        delnews.delete()
        return redirect(company)
        return reverse()
        
class UpdateTag(UpdateObjectsMixin, View):
    theformclass = TagForms
    model = Tag
    template = 'centralizer/tagupdate.html'
    
class UpdateCompany(UpdateObjectsMixin, View):
    theformclass = CompanyForms
    model = Company
    template = 'centralizer/compupdate.html'
    
class DeleteTag(DeleteObjectMixin, View):
    model = Tag
    success = reverse_lazy('centralizer_taglist')
    template = "centralizer/deltag.html"
    
class DeleteCompany(DeleteObjectMixin, View):
    model = Company
    success = reverse_lazy('centralizer_company_list')
    template = "centralizer/compdel.html"
    