from .views import CreateNews, UpdateNews, DeleteNews

urlpatterns = [    
    url(r'^create/$', CreateNews.as_view(), name='centralizer_create_related'),
    url(r'^update/$', UpdateNews.as_view(), name='centralizer_update_related'),
    url(r'^delete/$', DeleteNews.as_view(), name='centralizer_delete_news'),
]