from django.conf.urls import url 
from django.urls import path
from . import views
from . import api

urlpatterns = [
  path('<object_type>', api.object_list),
  path('<object_type>/<int:oid>', api.single_object),
  path('geodata/<table_name>/<param_values>/<excluded_values>/<keyword>/', api.filtered_geodata),
  path('geodata/<table_name>/<param_values>/<excluded_values>/', api.filtered_geodata),
  path('geodata/<table_name>/<param_values>/', api.filtered_geodata),
  path('geodata/<table_name>/', api.filtered_geodata),
]