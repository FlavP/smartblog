from django.conf.urls import url
from .views import EmailView

urlpatterns = [
    url(r'^$', EmailView.as_view(), name="contact"),
    ]