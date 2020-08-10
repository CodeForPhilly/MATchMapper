from django.conf.urls import url 
from django.urls import path, re_path
from . import views

urlpatterns = [
  url(r'^providers$', views.provider_list),
  re_path(r'^providers/(?P<provider_id>P\d{8})$', views.provider_item)
]