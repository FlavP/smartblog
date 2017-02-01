from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.views.decorators.http import require_http_methods
from .forms import ArticleForm

# Create your views here.
from .models import Article
@require_http_methods(['HEAD', 'GET'])
def article_details(request, year, month, slug):
    art = get_object_or_404(Article, added__year = year, added__month = month, art_slug = slug)
    return render(request,"blog/article_details.html",
                  {"article": art})

class ArticleList(View):

    template = "blog/article_list.html"
    def get(self, request):
        articles = Article.objects.all()
        context = {"article_list": articles}
        return render(request, self.template, context)

class CreateArticle(View):
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
        
class UpdateArticle(View):
    theformclass = ArticleForm
    template = "blog/artupdate.html"
    model = Article
    
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

class DeleteArticle(View):
    def get(self, request, year, month, slug):
        article = get_object_or_404(Article, added__year = year, added__month = month, art_slug = slug)
        return render(request, 'blog/artdel.html', {'article' : article})
    
    def post(self, request, year, month, slug):
        article = get_object_or_404(Article, added__year = year, added_month = month, art_slug = slug)
        article.delete()
        return redirect('blog_article_list')          
       
        