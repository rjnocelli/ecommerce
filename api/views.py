from django.shortcuts import render
from django.http import JsonResponse
# from .serializers import TaskSerializer
# from .models import Task

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/order-list/',
        'Detail View': '/order-detail/<str:pk>/',
        'Create': '/order-create/',
        'Update': '/order-update/<str:pk>/',
        'Delete': '/order-delete/<str:pk>/',        
    }
    
    return Response(api_urls)
