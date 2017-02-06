from django.conf.urls import url
from ..views import taglist, tagdetails, create_tag, CreateTag, DeleteTag, UpdateTag, TagList, PagedTag, TagDetails
from ..models import Tag

urlpatterns = [
    url(r'^create/$', CreateTag.as_view(), name='centralizer_create_tag'),
    url(r'^(?P<slug>[\w\-]+)/update/$', UpdateTag.as_view(), name='centralizer_update_tag'),
    url(r'^(?P<slug>[\w\-]+)/delete/$', DeleteTag.as_view(), name='centralizer_delete_tag'),
    url(r'^(?P<slug>[\w\-]+)/$', TagDetails.as_view(context_object_name = 'tag', template_name=("centralizer/tagdetails.html"), model = Tag), name="centralizer_tagdetails"),
    url((r'^(?P<page>\d+)/$'), PagedTag.as_view(), name="centralizer_tag_paged"),
    url(r'^$', TagList.as_view(), name="centralizer_taglist"),
    ]