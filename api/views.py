from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .serializers import OrderSerializer, ProductSerializer
from inventario_app.models import Order, Product

from itertools import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets, status



@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/order-list/',
        'Detail View': '/order-detail/<str:pk>/',
        'Create': '/order-create/',
        'Update': '/order-update/<str:pk>/',
        'Delete': '/order-delete/<str:pk>/',

        'Product-List': '/product-list/'        
    }
    return Response(api_urls)

# ORDER VIEWS -----

@api_view(['GET'])
def getActiveOrder(request):
    try:
        order = Order.objects.get(active = True)
        serializer = OrderSerializer(order)
    except:
        order = None
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

@api_view(['POST'])
def orderUpdate(request, id):
    order = Order.objects.get(id=id)
    serializer = OrderSerializer(instance=order, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def orderDelete(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# PRODUCT VIEWS -----

# @api_view(['GET'])
# def productList(request):
#     products = Product.objects.all()
#     most_popular = Product.objects.all().order_by("-views")[:4]
#     serializer = ProductSerializer(products, many=True)
#     serializer2 = ProductSerializer(most_popular, many=True)
#     return Response(serializer.data, serializer2.data)

# class productListView(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     def get_queryset(self):
#         products = Product.objects.all()
#         most_popular = Product.objects.all().order_by("-views")[:4]
#         return list(chain(products, most_popular))

class productList2(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

 

