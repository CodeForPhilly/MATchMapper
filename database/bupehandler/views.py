from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProviderSerializer
from .models import Provider
from rest_framework import status
from rest_framework.response import Response
import json
from django.core.exceptions import ObjectDoesNotExist

@api_view(["GET", "POST", "DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def provider_list(request):
    if request.method == 'GET':
        try:
            providers = Provider.objects.all()
            serializer = ProviderSerializer(providers, many=True)
            return JsonResponse({'providers': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    elif request.method == 'POST':
        payload = json.loads(request.body)
        try:
            provider = Provider.objects.create(
                first_name = payload["first_name"],
                last_name = payload["last_name"],
                prefix_name = payload["prefix_name"],
                suffix = payload["suffix"],
                degree = payload["degree"],
                who_id = payload["who_id"],
                est_rx_cap = payload["est_rx_cap"],
                patient_max = payload["patient_max"]
            )
            serializer = ProviderSerializer(provider)
            return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        try:
            providers = Provider.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(["GET", "PUT", "DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def provider_item(request, provider_id):
    if request.method == "GET":
        try:
            provider = Provider.objects.get(provider_id=provider_id)
            serializer = ProviderSerializer(provider)
            return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "PUT":
        payload = json.loads(request.body)
        try:
            provider_item = Provider.objects.filter(provider_id=provider_id)
            # returns 1 or 0
            provider_item.update(**payload)
            provider = Provider.objects.get(provider_id=provider_id)
            serializer = ProviderSerializer(provider)
            return JsonResponse({'provider': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        try:
            provider = Provider.objects.get(provider_id=provider_id)
            print('hit')
            provider.delete()
            print('hit')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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