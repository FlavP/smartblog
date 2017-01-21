from django.conf.urls import url
from blog.views import ArticleList
from .views import taglist, tagdetails, companies, company_details, create_tag

urlpatterns = [
    url(r'^tag/$', taglist, name="centralizer_taglist"),
    # Acest artificiu este facut pentru a denumi un grup (un segment al expresiei regulate)
    # pentru a-l trimite functiei tagdetails ca parametru
    # daca url-ul nostru este http://127.0.0.1:8000/tag/django, noi apelam tagdetails(request, slug='django')
    # also a good idea is to name your url
    url(r'^tag/create/$', create_tag, name='centralizer_create_tag'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', tagdetails, name='centralizer_tagdetails'),
    url(r'^companies/$', companies, name='centralizer_company_list'),
    url(r'companies/(?P<slug>[\w\-]+)/$', company_details, name="centralizer_company_details"),
]