from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, ListView, YearArchiveView, MonthArchiveView, ArchiveIndexView, DetailView, DeleteView
from core.utils import UpdateView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from .forms import ArticleForm
from .utils import DateObjectMixin

# Create your views here.
from .models import Article
from .utils import GetArticleMixin
@require_http_methods(['HEAD', 'GET'])

def article_details(request, year, month, slug):
    art = get_object_or_404(Article, added__year = year, added__month = month, art_slug = slug)
    return render(request,"blog/article_details.html",
                  {"article": art})



class ArticleList(ArchiveIndexView):
    allow_empty = True # allow display empty
    allow_future = True # allow object with dates in the future
    context_object_name = 'article_list'
    date_field = 'added'
    make_object_list = True
    model = Article
    paginate_by = 5
    template_name = "blog/article_list.html"
    def get(self, request):
        articles = Article.objects.all()
        context = {"article_list": articles}
        return render(request, self.template, context)

class ArticleDetails(DetailView, GetArticleMixin):
    model = Article
    allow_future = True
    date_field = 'added'

'''
modul de dinainte de mixin
class ArticleDetails(DateDetailView):
    date_field = 'added'
    model = Article
    month_format = '%m'

    def get_day(self):
        return 1

    def _make_single_date_lookup(self, date):
        date_field = self.get_date_field()
        return {
            date_field + '__year': date.year,
            date_field + '__month': date.month,
        }
'''

class CreateArticle(CreateView):
    theformclass = ArticleForm
    template = "blog/artcreate.html"

    def get(self, request):
        return render(request, self.template, {'theform': self.theformclass})

    def post(self, request):
        thebounded_form = self.theformclass
        if thebounded_form.is_valid():
            new_article = thebounded_form.save()
            return redirect(new_article)
        else:
            return render(request, self.template, {'theform': self.theformclass})
        
class UpdateArticle(UpdateView, GetArticleMixin):
    #inherit GetArticleMixin for identification with year, month, slug
    form_class = ArticleForm
    model = Article
    allow_future = True
    date_field = 'added'
#old one bellow
'''    
    def take_object(self, year, month, art_slug):
        return get_object_or_404(
            model = self.model,
            added__year=year,
            added__month=month,
            art_slug=art_slug) 
    
    def get(self, request, year, month, art_slug):
        article = self.take_object(year, month, art_slug)
        #ne mai trebuie un context in care sa plasam obiectul-articol  de mai sus, gaist sau nu in baza de date
        #in context avem obiectul formulat pe care il instantiem cu obiectul-articol pe care vrem sa-l modificam
        context = {"theform": self.theformclass(instance=article),
                   "article": article}
        return render(request, self.template, context)
    
    def post(self, request, year, month, art_slug):
        article = self.take_object(year, month, art_slug)
        bounded_form = self.theformclass(request.POST, instance=article)
        if bounded_form.is_valid():
            new_article = bounded_form.save()
            return redirect(new_article)
        else:
            context = {"theform": self.theformclass(instance=article),
                       "article": article}
            return render(request, self.template, context)
'''
class DeleteArticle(DeleteView, DateObjectMixin):
    model = Article
    date_field = 'added'
    allow_future = True
    #delete has to have a redirect page that redirects you if the request is succesful
    success_url = reverse_lazy('blog_article_list')

'''
#old DeleteArticle
class DeleteArticle(View):
    def get(self, request, year, month, slug):
        article = get_object_or_404(Article, added__year = year, added__month = month, art_slug = slug)
        return render(request, 'blog/artdel.html', {'article' : article})
    
    def post(self, request, year, month, slug):
        article = get_object_or_404(Article, added__year = year, added_month = month, art_slug = slug)
        article.delete()
        return redirect('blog_article_list')          
'''

class YearlyOrdered(YearArchiveView):
    model = Article
    date_field = 'added'
    make_object_list = True

class MonthlyOrdered(MonthArchiveView):
    model = Article
    date_field = 'added'
    month_format = '%m'