from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import Sitecodes_samhsa_ftlocSerializer, Siterecs_samhsa_ftlocSerializer, Siterecs_samhsa_otpSerializer, Siterecs_dbhids_tadSerializer, Siterecs_other_srcsSerializer, Sites_allSerializer
from .models import Sitecodes_samhsa_ftloc, Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Siterecs_other_srcs, Sites_all
from .scrapers.samhsa_bupe_locator_scraper import main as scrape_samhsa
from rest_framework import status
from rest_framework.response import Response
import json
from django.core.exceptions import ObjectDoesNotExist

object_type_dict = {
    'sitecodes_samhsa_ftloc': (Sitecodes_samhsa_ftloc, Sitecodes_samhsa_ftlocSerializer),
    'siterecs_samhsa_ftloc': (Siterecs_samhsa_ftloc, Siterecs_samhsa_ftlocSerializer),
    'siterecs_samhsa_otp': (Siterecs_samhsa_otp, Siterecs_samhsa_otpSerializer),
    'siterecs_dbhids_tad': (Siterecs_dbhids_tad, Siterecs_dbhids_tadSerializer),
    'siterecs_other_srcs': (Siterecs_other_srcs, Siterecs_other_srcsSerializer),
    'sites_all': (Sites_all, Sites_allSerializer)
}

@api_view(["GET", "POST", "PUT", "DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def object_list(request, object_type):
    if object_type_dict.get(object_type) is None:
        return JsonResponse({'error': 'Object not found'}, safe=False, status=status.HTTP_404_NOT_FOUND)    
    object_model = object_type_dict[object_type][0]
    object_serializer = object_type_dict[object_type][1]
    if request.method == 'GET':
        try:
            all_objects = object_model.objects.all()
            serializer = object_serializer(all_objects, many=True)
            return JsonResponse({'objects': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    elif request.method == 'POST':
        payload = json.loads(request.body)
        try:
            new_object = object_model(**payload)
            new_object.save()
            serializer = object_serializer(new_object)
            return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('%s (%s)' % (e.message, type(e)))
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        try:
            all_objects = object_model.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(["GET", "PUT", "DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def single_object(request, object_type, oid):
    if object_type_dict.get(object_type) is None:
        return JsonResponse({'error': 'Object not found'}, safe=False, status=status.HTTP_404_NOT_FOUND)    
    object_model = object_type_dict[object_type][0]
    object_serializer = object_type_dict[object_type][1]
    if request.method == "GET":
        try:
            this_object = object_model.objects.get(oid=oid) # TODO need to standardize id so that we can use generic keyword argument instead of provider_id
            serializer = object_serializer(this_object)
            return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "PUT":
        payload = json.loads(request.body)
        try:
            this_object = object_model.objects.filter(oid=oid)
            # returns 1 or 0
            this_object.update(**payload)
            this_object = object_model.objects.get(oid=oid)
            serializer = object_serializer(this_object)
            return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        try:
            this_object = object_model.objects.get(oid=oid)
            this_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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