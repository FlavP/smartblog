from django.conf.urls import url
from blog.views import ArticleList
from .views import taglist, tagdetails, \
    companies, company_details, create_tag, CreateTag, CreateCompany, CreateNews, UpdateNews, \
    UpdateTag, UpdateCompany, DeleteNews, DeleteTag, DeleteCompany

urlpatterns = [
    url(r'^tag/$', taglist, name="centralizer_taglist"),
    # Acest artificiu este facut pentru a denumi un grup (un segment al expresiei regulate)
    # pentru a-l trimite functiei tagdetails ca parametru
    # daca url-ul nostru este http://127.0.0.1:8000/tag/django, noi apelam tagdetails(request, slug='django')
    # also a good idea is to name your url
    url(r'^tag/create/$', CreateTag.as_view(), name='centralizer_create_tag'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$', UpdateTag.as_view(), name='centralizer_update_tag'),
    url(r'^tag/(?P<slug>[\w\-]+)/delete/$', DeleteTag.as_view(), name='centralizer_delete_tag'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', tagdetails, name='centralizer_tagdetails'),
    url(r'^companies/$', companies, name='centralizer_company_list'),
    url(r'^news/create/$', CreateNews.as_view(), name='centralizer_create_related'),
    url(r'^news/update/$', UpdateNews.as_view(), name='centralizer_update_related'),
    url(r'^news/delete/$', DeleteNews.as_view(), name='centralizer_delete_news'),
    url(r'^companies/create/$', CreateCompany.as_view(), name='centralizer_create_company'),
    url(r'^companies/(?P<slug>[\w\-]+)/update/$', UpdateCompany.as_view(), name='centralizer_update_company'),
    url(r'^companies/(?P<slug>[\w\-]+)/delete/$', DeleteCompany.as_view(), name='centralizer_delete_company'),
    url(r'companies/(?P<slug>[\w\-]+)/$', company_details, name="centralizer_company_details"),
]