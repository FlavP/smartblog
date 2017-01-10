from django.conf.urls import url
from .views import ArticleList, article_details


urlpatterns = [
    url(r'^$', ArticleList.as_view(), name="blog_article_list"),
    url(r'^(?P<year>\d{4})/'
        r'^(?P<month>\d{1,2})/'
        r'^(?P<slug>[\w\-]+)/$',
        article_details, {'parent_template': 'base.html'}, name="blog_article_details"),
]