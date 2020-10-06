from django.shortcuts import render
from django.http import JsonResponse
from .serializers import OrderSerializer
from inventario_app.models import Order

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

@api_view(['GET'])
def orderList(request):
    orders = Order.objects.all().order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def orderDetail(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['POST'])
def orderCreate(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# @api_view(['POST'])
# def taskUpdate(request, id):
#     task = Task.objects.get(id=id)
#     serializer = TaskSerializer(instance=task, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def taskDelete(request, id):
#     task = Task.objects.get(id=id)
#     print(task)
#     task.delete()
#     return Response("Y se borro!!!!")
