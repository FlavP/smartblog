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
from django.conf.urls import url, include
from django.contrib import admin
from centralizer.urls import (relatednews as rel_urls, company as co_urls, tag as tag_urls)
from blog import urls as blurls
from contact import urls as curls
from .views import redir
from django.contrib.flatpages import urls as flurl

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #nu mai pui $ la sfarsit, atentie atentie atentie!!!
    url(r'^related/', include(rel_urls)),
    url(r'^tag/', include(tag_urls)),
    url(r'^company/', include(co_urls)),
    #url(r'^page', include(flurl)),
    url(r'^blog/', include(blurls)),
    url(r'^contact/', include(curls)),
    #nici aici nu pui $ la sfarsit, you have been warned
    url(r'^', include(flurl)),
]
