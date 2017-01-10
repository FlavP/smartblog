from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.decorators.http import require_http_methods

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