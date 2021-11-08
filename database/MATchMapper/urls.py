"""MATchMapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.shortcuts import render
from bupehandler import views

from django.views.decorators.cache import cache_page
cache_duration = 60

def render_react(request):
    return render(request, "index.html")

urlpatterns = [
    path("/", render_react),
    path('admin/', admin.site.urls),
    url('api-auth/', include('rest_framework.urls')),
    url('api/', include('bupehandler.urls')),
    re_path(r"table\/", render_react),
    re_path(r"map\/", render_react),
    # url(r'^headless/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)/(?P<keyword>.+)/$', views.headless_query, name="headless"),
    url(r'^headless/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)/(?P<keyword>.+)/$', views.headless_query, name="headless"),
    url(r'^headless/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)/$', views.headless_query, name="headless"),
    url(r'^headless/(?P<table_name>.+)/(?P<param_values>.+)/$', views.headless_query, name="headless"),
    url(r'^headless/(?P<table_name>.+)/$',views.headless_query, name = "headless"),
]