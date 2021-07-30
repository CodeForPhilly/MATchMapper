from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from .serializers import ProviderSerializer
# from .models import Provider
from .scrapers.samhsa_bupe_locator_scraper import main as scrape_samhsa
from rest_framework import status
from rest_framework.response import Response
import json
from django.core.exceptions import ObjectDoesNotExist
from .serializers import Sitecodes_samhsa_ftlocSerializer, Siterecs_samhsa_ftlocSerializer, Siterecs_samhsa_otpSerializer, Siterecs_dbhids_tadSerializer, Ba_dbhids_tadSerializer, Siterecs_other_srcsSerializer, Sites_allSerializer, Siterecs_hfp_fqhcSerializer
from .models import Sitecodes_samhsa_ftloc, Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Ba_dbhids_tad, Siterecs_other_srcs, Sites_all, Siterecs_hfp_fqhc, Table_info
import re 
from spellchecker import SpellChecker
from .model_translation import Sites_general_display
from .model_translation import filterKeyToLocalKey
from django.forms.models import model_to_dict
from django.db.models import CharField
from django.db.models import  Q
from .tableCaching import fetchCachedIfRecent
import re


@api_view(["GET", "POST", "DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def sites_all_display(request): 
    sites_all_objects = Sites_all.objects.all()
    print(sites_all_objects)
    sites_all_serializer = Sites_allSerializer(sites_all_objects, many=True)
    return render(request,"bupehandler/list_all.html", {"title": 'sites_all', "sites_all" : sites_all_serializer.data})

@api_view(["GET", "POST", "DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def siterecs_samhsa_otp_display(request, filter_params=None, order_by_params=None):
    order_param = ['program_name']
    filter_params={'program_name': 'Achievement Through Counseling and Treatment (ACT 1)'}
    siterecs_samhsa_otp_objects = Siterecs_samhsa_otp.objects.all()
    if filter_params:
        siterecs_samhsa_otp_objects = siterecs_samhsa_otp_objects.filter(**filter_params)
    if order_by_params:
        for order_param in order_by_params:
            siterecs_samhsa_otp_objects = siterecs_samhsa_otp_objects.order_by(order_param)
    # siterecs_samhsa_otp_objects = siterecs_samhsa_otp_objects.order_by('name_program')
    print(siterecs_samhsa_otp_objects)
    siterecs_samhsa_otp_serializer = Siterecs_samhsa_otpSerializer(siterecs_samhsa_otp_objects, many=True)
    return render(request,"bupehandler/list_all.html", {"title": 'siterecs_samhsa_otp_display', "objects" : siterecs_samhsa_otp_serializer.data})

@api_view(["GET", "POST", "DELETE"])
@csrf_exempt
def filtered_table(request, table_name, param_values=None, excluded_values=None, keyword = None):
    #example default param url: http://127.0.0.1:8000/table/siterecs_samhsa_ftloc/state_usa=PA&bu=True/, this url retrieves row form siterecs_samhsa_ftloc that has state_usa= PA and bu = True. Add as many paramters as you want
    #if you want to autofill all of your parameter values, then put autofill=True as a param_values pair in your url. Example: http://127.0.0.1:8000/table/siterecs_samhsa_ftloc/name1=Casa&autofill=True. This would match all rows that have name1 values contain Casa.
    #if you want to autocorrect all of your parameter values, then put autocorrect=True as a param_values pair in your url. Example: http://127.0.0.1:8000/table/siterecs_samhsa_ftloc/city=philadelphi&autocorrect=True. This would correct philadelphi to Philadelphia.
    #You can use both autocorrect and autofill. This will correct the param and THEN, autofill. Example: http://127.0.0.1:8000/table/siterecs_samhsa_ftloc/name2=behavor&autocorrect=True&autofill=True. This will correct behavor to behaviour and then autofill behavior to display "Behavioral Healthcare Center" and "Behavioral Health Services"
    #All of our queries are case insensitive.
    #The NOT filter is put after the normal filter:
    #Example of using the NOT filter: http://127.0.0.1:8000/table/siterecs_samhsa_ftloc/None/tele=True : all sites with tele not True
    #Another one using the NOT filter: http://127.0.0.1:8000/table/siterecs_samhsa_ftloc/state_usa%3DPA&bu%3DTrue/tele=True : all sites in PA, bu = True, with tele not True.
    print(table_name)
    print(param_values)
    print(excluded_values)
    autofill = False
    autocorrect=False
    filter_params = {"archival_only":False}
    excluded_params = {}
    if param_values:
        if param_values != "None":
            query_pairs = param_values.split("&")
            for pair in query_pairs:
                list_pair = pair.split("=")
                list_pair[0] = filterKeyToLocalKey(list_pair[0], table_name)
                if list_pair[1] == "None":
                    list_pair[1] = None
                if list_pair[0] == "autofill" and list_pair[1] == "True":
                    autofill = True
                elif list_pair[0] == "autocorrect" and list_pair[1] == "True":
                    autocorrect = True  
                else:
                    filter_params['%s__iexact' % list_pair[0]] = list_pair[1]
    if excluded_values:
        if excluded_values != "None": 
            query_pairs = excluded_values.split("&")
            for pair in query_pairs:
                list_pair = pair.split("=")
                list_pair[0] = filterKeyToLocalKey(list_pair[0], table_name)
                if list_pair[1] == "None":
                    list_pair[1] = None
                else:
                    excluded_params[list_pair[0]] = list_pair[1]
    #change query dictionary if autocorrect is on
    if autocorrect:
        spell = SpellChecker()
        autocorrect_filter_params = {}
        for key in filter_params:
            if filter_params[key] == None:
                autocorrect_filter_params[key] = None
            else:
                autocorrect_filter_params[key] = spell.correction(filter_params[key])
        filter_params= autocorrect_filter_params
    #change query dictionary if autofill is on
    if autofill:
        autofill_filter_params = {}
        for key in filter_params:
            if filter_params[key] == None:
                autofill_filter_params[key] = None
            else:
                autofill_filter_params['%s__icontains' % key.split("__",1)[0]] = filter_params[key]
        filter_params = autofill_filter_params
    table_dict = {
        "sitecodes_samhsa_ftloc": Sitecodes_samhsa_ftloc,
        "siterecs_samhsa_ftloc": Siterecs_samhsa_ftloc,
        "siterecs_hfp_fqhc": Siterecs_hfp_fqhc,
        "siterecs_samhsa_otp": Siterecs_samhsa_otp ,
        "siterecs_dbhids_tad": Siterecs_dbhids_tad,
        "ba_dbhids_tad": Ba_dbhids_tad,
        "siterecs_other_srcs" : Siterecs_other_srcs ,
        "sites_all" : Sites_all,
    }
    serializer_dict = {
        "sitecodes_samhsa_ftloc" : Sitecodes_samhsa_ftlocSerializer,
        "siterecs_samhsa_ftloc" : Siterecs_samhsa_ftlocSerializer,
        "siterecs_hfp_fqhc": Siterecs_hfp_fqhcSerializer,
        "siterecs_samhsa_otp": Siterecs_samhsa_otpSerializer,
        "siterecs_dbhids_tad": Siterecs_dbhids_tadSerializer,
        "ba_dbhids_tad": Ba_dbhids_tadSerializer,
        "siterecs_other_srcs" : Siterecs_other_srcsSerializer,
        "sites_all" : Sites_allSerializer,
    }
    table_objects = table_dict[table_name].objects.all().filter(**filter_params)
    # table_objects = fetchCachedIfRecent(table_name, ttl=300).filter(**filter_params)
    for excluded_param in excluded_params:
        current_excluded_param = {}
        current_excluded_param[excluded_param] = excluded_params[excluded_param]
        table_objects=table_objects.exclude(**current_excluded_param)
    if keyword != None: 
        fields = [f for f in table_dict[table_name]._meta.fields if isinstance(f, CharField)]
        queries = [Q(**{f.name + "__icontains": keyword}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        table_objects = table_objects.filter(qs)
    if request.GET.getlist('order'):
        order_by_list = request.GET.getlist('order')
        table_objects = table_objects.order_by(*order_by_list)
    general_display_list = []
    for table_object in table_objects:
        dicted = table_object.__dict__
        generalDisplayed = Sites_general_display(table_name, dicted)
        # print(generalDisplayed.output["full_certification"])
        general_display_list.append(generalDisplayed.output)
    table_info = Table_info.objects.get(table_name=table_name).__dict__
    #table_serializer = serializer_dict[table_name](table_objects, many=True)
    #print(general_display_list[0].keys())
    return render(request,"bupehandler/list_all.html", {"title": table_name, "objects" : general_display_list, "table_info": table_info})


@api_view(["GET", "POST", "DELETE"])
@csrf_exempt
def default_map(request):
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(request, 'bupehandler/map.html', { 'mapbox_access_token': mapbox_access_token })

@api_view(["GET", "POST", "DELETE"])
@csrf_exempt
def filtered_map(request, table_name, param_values="", excluded_values="", keyword = ""):
    naming_dict = { 
        "sitecodes_samhsa_ftloc" : "service_name",
        "siterecs_samhsa_ftloc" : "name1",
        "siterecs_samhsa_otp": "program_name",
        "siterecs_dbhids_tad": "name1", 
        "ba_dbhids_tad": "name_ba", 
        "siterecs_hfp_fqhc": "name_short", 
        "siterecs_other_srcs" : "name1", 
        "sites_all" : "name1",
        "Siterecs_dbhids_tads": "name1"
    }
    mapbox_access_token = 'pk.my_mapbox_access_token'
    table_info = Table_info.objects.get(table_name=table_name).__dict__
    if param_values: 
        #paramList = [paramString.split("=") for paramString in re.split("&amp;|&", param_values)]
        #for param in paramList:
        #    param[0] = filterKeyToLocalKey(param[0], table_name)
        #param_values = "&".join(["=".join(param) for param in paramList])

        #exclusionList = [exclusionString.split("=") for exclusionString in re.split("&amp;|&", param_values)]
        #for exclusion in exclusionList:
        #    exclusion[0] = filterKeyToLocalKey(exclusion[0], table_name)
        #excluded_values = "&".join(["=".join(exclusion) for exclusion in exclusionList])

        return render(request, 'bupehandler/filtered_map.html', { 'mapbox_access_token': mapbox_access_token, "table_name": table_name, "table_info": table_info, "param_values": param_values, "excluded_values": excluded_values, "destination_name": naming_dict[table_name], "keyword": keyword})
    else: 
        return render(request, 'bupehandler/filtered_map.html', { 'mapbox_access_token': mapbox_access_token, "table_name": table_name, "table_info": table_info, "destination_name": naming_dict[table_name], "keyword": keyword})

# @api_view(["GET", "POST", "DELETE"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def provider_list(request):
#     if request.method == 'GET':
#         try:
#             providers = Provider.objects.all()
#             serializer = ProviderSerializer(providers, many=True)
#             return JsonResponse({'providers': serializer.data}, safe=False, status=status.HTTP_200_OK)
#         except Exception:
#             return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
#     elif request.method == 'POST':
#         payload = json.loads(request.body)
#         try:
#             provider = Provider.objects.create(
#                 first_name = payload["first_name"],
#                 last_name = payload["last_name"],
#                 prefix_name = payload["prefix_name"],
#                 suffix = payload["suffix"],
#                 degree = payload["degree"],
#                 who_id = payload["who_id"],
#                 est_rx_cap = payload["est_rx_cap"],
#                 patient_max = payload["patient_max"]
#             )
#             serializer = ProviderSerializer(provider)
#             return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     elif request.method == 'DELETE':
#         try:
#             providers = Provider.objects.all().delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

# @api_view(["GET", "PUT", "DELETE"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def provider_item(request, provider_id):
#     if request.method == "GET":
#         try:
#             provider = Provider.objects.get(provider_id=provider_id)
#             serializer = ProviderSerializer(provider)
#             return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     elif request.method == "PUT":
#         payload = json.loads(request.body)
#         try:
#             provider_item = Provider.objects.filter(provider_id=provider_id)
#             # returns 1 or 0
#             provider_item.update(**payload)
#             provider = Provider.objects.get(provider_id=provider_id)
#             serializer = ProviderSerializer(provider)
#             return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     elif request.method == "DELETE":
#         try:
#             provider = Provider.objects.get(provider_id=provider_id)
#             print('hit')
#             provider.delete()
#             print('hit')
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(["GET", "POST", "DELETE"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def provider_update_list(request):
#     if request.method == 'GET':
#         samhsa_data = scrape_samhsa()
#         return JsonResponse({'providers': samhsa_data}, safe=False, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         payload = json.loads(request.body)
#         try:
#             provider = Provider.objects.create(
#                 first_name = payload["first_name"],
#                 last_name = payload["last_name"],
#                 prefix_name = payload["prefix_name"],
#                 suffix = payload["suffix"],
#                 degree = payload["degree"],
#                 who_id = payload["who_id"],
#                 est_rx_cap = payload["est_rx_cap"],
#                 patient_max = payload["patient_max"]
#             )
#             serializer = ProviderSerializer(provider)
#             return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     elif request.method == 'DELETE':
#         try:
#             providers = Provider.objects.all().delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         except Exception:
#             return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def add_all_providers(request):
#     payload_list = json.loads(request.body)
#     serialized_data_list = []
#     try:
#         for pay_load in payload_list:
#             provider = Provider.objects.create(
#                 first_name = payload["first_name"],
#                 last_name = payload["last_name"],
#                 prefix_name = payload["prefix_name"],
#                 suffix = payload["suffix"],
#                 degree = payload["degree"],
#                 who_id = payload["who_id"],
#                 est_rx_cap = payload["est_rx_cap"],
#                 patient_max = payload["patient_max"]
#             )
#             # TODO figure out how to return JsonResponse with multiple providers in a python list
#             serializer = ProviderSerializer(provider)
#             serialized_data_list.append(serializer)
#         return JsonResponse({'providers': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#     except Exception:
#         return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def add_provider(request):
#     payload = json.loads(request.body)
#     try:
#         provider = Provider.objects.create(
#             first_name = payload["first_name"],
#             last_name = payload["last_name"],
#             prefix_name = payload["prefix_name"],
#             suffix = payload["suffix"],
#             degree = payload["degree"],
#             who_id = payload["who_id"],
#             est_rx_cap = payload["est_rx_cap"],
#             patient_max = payload["patient_max"]
#         )
#         serializer = ProviderSerializer(provider)
#         return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#     except Exception:
#         return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["PUT"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def update_provider(request, provider_id):
#     payload = json.loads(request.body)
#     try:
#         provider_item = Provider.objects.filter(provider_id=provider_id)
#         # returns 1 or 0
#         provider_item.update(**payload)
#         provider = Provider.objects.get(provider_id=provider_id)
#         serializer = ProviderSerializer(provider)
#         return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#     except Exception:
#         return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(["DELETE"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])
# def delete_provider(request, provider_id):
#     try:
#         provider = Provider.objects.get(provider_id=provider_id)
#         provider.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#     except Exception:
#         return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
