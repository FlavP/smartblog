"""smartblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from centralizer.views import home, tagdetails

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home),
    #Acest artificiu este facut pentru a denumi un grup (un segment al expresiei regulate)
    #pentru a-l trimite functiei tagdetails ca parametru
    #daca url-ul nostru este http://127.0.0.1:8000/tag/django, noi apelam tagdetails(request, slug='django')
    #also a good idea is to name your url
    url(r'^tag/(?P<slug>[\w\-]+)/$', tagdetails, name='centralizer_tagdetails'),
]
