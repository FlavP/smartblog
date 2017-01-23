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
        return render(request, self.template,
                      {"article_list": Article.objects.all()})

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