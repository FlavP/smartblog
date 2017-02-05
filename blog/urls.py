from django.conf.urls import url
from .views import ArticleList, article_details, CreateArticle, UpdateArticle, DeleteArticle


urlpatterns = [
    url(r'^create/$', CreateArticle.as_view(), name="blog_article_create"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[\w\-]+)/update/$',
         UpdateArticle.as_view(), name="blog_article_update"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[\w\-]+)/delete/$', DeleteArticle.as_view(), name="blog_article_delete"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[\w\-]+)/$',
        article_details, {'parent_template': 'base.html'}, name="blog_article_details"),
    #url(r'^$', ArticleList.as_view(), name="blog_article_list"),
]