from django.conf.urls import url
from ..views import taglist, tagdetails, create_tag, CreateTag, DeleteTag, UpdateTag, TagList, PagedTag

urlpatterns = [
    url(r'^create/$', CreateTag.as_view(), name='centralizer_create_tag'),
    url(r'^(?P<slug>[\w\-]+)/update/$', UpdateTag.as_view(), name='centralizer_update_tag'),
    url(r'^(?P<slug>[\w\-]+)/delete/$', DeleteTag.as_view(), name='centralizer_delete_tag'),
    url(r'^(?P<slug>[\w\-]+)/$', tagdetails, name='centralizer_tagdetails'),  
    url(r'^$', TagList.as_view(), name="centralizer_taglist"),
    url((r'^(?P<page>\d+)/$'), PagedTag.as_view(), name="centralizer_tag_paged")
    ]