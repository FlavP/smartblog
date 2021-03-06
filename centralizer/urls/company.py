from django.conf.urls import url
from centralizer.views import companies, company_details, CreateCompany, DeleteCompany, UpdateCompany, CompanyList, \
    CompanyDetails, DeleteNews, UpdateNews, CreateNews, RelatedNewsCreate
from centralizer.models import Company
    
urlpatterns = [
    url(r'^create/$', CreateCompany.as_view(), name='centralizer_create_company'),
    url(r'^(?P<slug>[\w\-]+)/update/$', UpdateCompany.as_view(), name='centralizer_update_company'),
    url(r'^(?P<slug>[\w\-]+)/delete/$', DeleteCompany.as_view(), name='centralizer_delete_company'),
    url(r'^(?P<slug>[\w\-]+)/$', CompanyDetails.as_view(context_object_name = 'company', template_name=("centralizer/company_details.html"), model = Company), name="centralizer_company_details"),
    url(r'^(P<company_slug>[\w\-]+)/add_article_link/$', RelatedNewsCreate.as_view(), name="centralizer_create_related"),
    url(r'^(P<company_slug>[\w\-]+)/(P<news_slug>[\w\-]+)/delete/$', DeleteNews.as_view(), name="centralizer_delete_related"),
    url(r'^(P<company_slug>[\w\-]+)/(P<news_slug>[\w\-]+)/update/$', UpdateNews.as_view(), name="centralizer_update_related"),
    url(r'^$', CompanyList.as_view(), name='centralizer_company_list'),
    ]