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
from .serializers import Sitecodes_samhsa_ftlocSerializer, Siterecs_samhsa_ftlocSerializer, Siterecs_samhsa_otpSerializer, Siterecs_dbhids_tadSerializer, Siterecs_other_srcsSerializer, Sites_allSerializer
from .models import Sitecodes_samhsa_ftloc, Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Siterecs_other_srcs, Sites_all


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
    order_param = ['name_program']
    filter_params={'name_program': 'Achievement Through Counseling and Treatment (ACT 1)'}
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
def table(request, table_name, param_values): 
    query_pairs = param_values.split("&")
    filter_params = {}
    for pair in query_pairs: 
        list_pair = pair.split("=")
        filter_params[list_pair[0]] = list_pair[1]
    #list_param_values = param_values.split("&") 
    #list_param_types = param_types.split("&")
    #for i in range(len(list_param_values)): 
    #    filter_params[list_param_types[i]] = list_param_values[i]
    table_dict = { 
        "sitecodes_samhsa_ftloc": Sitecodes_samhsa_ftloc, 
        "siterecs_samhsa_ftloc": Siterecs_samhsa_ftloc, 
        "siterecs_samhsa_otp": Siterecs_samhsa_otp ,
        "siterecs_dbhids_tad": Siterecs_dbhids_tad, 
        "siterecs_other_srcs" : Siterecs_other_srcs , 
        "sites_all" : Sites_all,
    }
    serializer_dict = { 
        "sitecodes_samhsa_ftloc" : Sitecodes_samhsa_ftlocSerializer,
        "siterecs_samhsa_ftloc" : Siterecs_samhsa_ftlocSerializer, 
        "siterecs_samhsa_otp": Siterecs_samhsa_otpSerializer, 
        "siterecs_dbhids_tad": Siterecs_dbhids_tadSerializer, 
        "siterecs_other_srcs" : Siterecs_other_srcsSerializer, 
        "sites_all" : Sites_allSerializer,
    }
    table_objects = table_dict[table_name].objects.all()
    if filter_params:
        table_objects = table_objects.filter(**filter_params)
    table_serializer = serializer_dict[table_name](table_objects, many=True)
    return render(request,"bupehandler/list_all.html", {"title": table_name, "objects" : table_serializer.data})


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