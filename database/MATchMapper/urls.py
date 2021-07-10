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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from bupehandler import views

from django.views.decorators.cache import cache_page
cache_duration = 60

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api-auth/', include('rest_framework.urls')),
    url('api/', include('bupehandler.urls')),
    url(r'^table/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)/(?P<keyword>.+)$', views.filtered_table, name="filtered_table"),
    url(r'^table/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)$', views.filtered_table, name="filtered_table"),
    url(r'^table/(?P<table_name>.+)/(?P<param_values>.+)/$', views.filtered_table, name="filtered_table"),
    url(r'^table/(?P<table_name>.+)/$',views.filtered_table, name = "filtered_table"),
    url(r'^map/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)/(?P<keyword>.+)$', views.filtered_map, name="filtered_map"),
    url(r'^map/(?P<table_name>.+)/(?P<param_values>.+)/(?P<excluded_values>.+)$', views.filtered_map, name="filtered_map"),
    url(r'^map/(?P<table_name>.+)/(?P<param_values>.+)/$', views.filtered_map, name="filtered_map"),
    url(r'^map/(?P<table_name>.+)/$', views.filtered_map, name="filtered_map"), 
]
