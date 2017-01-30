from django.conf.urls import url
from ..views import companies, company_details, \
CreateCompany, DeleteCompany, UpdateCompany, CompanyList
    
urlpatterns  = [    
    url(r'^create/$', CreateCompany.as_view(), name='centralizer_create_company'),
    url(r'^(?P<slug>[\w\-]+)/update/$', UpdateCompany.as_view(), name='centralizer_update_company'),
    url(r'^(?P<slug>[\w\-]+)/delete/$', DeleteCompany.as_view(), name='centralizer_delete_company'),
    url(r'^(?P<slug>[\w\-]+)/$', company_details, name="centralizer_company_details"),
    url(r'^$', CompanyList.as_view(), name='centralizer_company_list')
    ]