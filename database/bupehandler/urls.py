from django.conf.urls import url 
from django.urls import path
from . import views
from . import api

urlpatterns = [
  path('<object_type>', api.object_list),
  path('<object_type>/<int:oid>', api.single_object)
]