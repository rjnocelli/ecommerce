from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from api.serializers import (
    OrderSerializer,
    ProductSerializer,
    ServerToClientProductSerializer,
    ServerToClientOrderSerializer,
    ServerToClientCategorySerializer,
    ServerToClientProductSerializerOnSearch,)
from inventario_app.models import Order, Product, Category
from django.db.models import Q

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

        'Product-List': '/product-list/',
        'Popular-Products': '/popular-products/',

        'Categories-List': '/categories-list/',
    }
    return Response(api_urls)

# ORDER VIEWS -----

@api_view(['GET'])
def getAllOrders(request):
    try:
        order = Order.objects.all()
        serializer = ServerToClientOrderSerializer(order, many=True)
    except:
        order = None
    return Response(serializer.data)

@api_view(['GET'])
def orderDetail(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])
def orderDelete(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def orderUpdate(request, id):
    order = Order.objects.get(id=id)
    serializer = OrderSerializer(instance=order, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    

@api_view(['GET'])
def getProductsOnSearch(request):
    query = request.query_params['q']
    products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    serializer = ServerToClientProductSerializerOnSearch(products, many=True)
    return Response(serializer.data)


# PRODUCT VIEWS ------

def infinite_filter(request):
        limit = request.GET.get('limit')    
        offset = request.GET.get('offset')
        return Product.objects.all()[int(offset): int(offset) + int(limit)]

def has_more(request):
        offset = request.GET.get('offset')
        if int(offset) > Product.objects.all().count():
            return False
        return True

class infinte_scroll_view(generics.ListAPIView):
    serializer_class = ServerToClientProductSerializer

    def get_queryset(self):
        return infinite_filter(self.request)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'products':serializer.data,
            'has_more': has_more(request)
            })

@api_view(['GET'])
def getAllProducts(request):
    return Response(ServerToClientProductSerializer(Product.objects.filter(in_stock=True).order_by("-is_bundle", "-views"), many=True).data)

@api_view(['GET'])
def getMostPopularProducts(request):
    """
    Returns a JSON file containing the 4 most popular products ordered by views
    and all products.
    """
    return Response(ServerToClientProductSerializer(Product.objects.all().filter(in_stock=True).order_by("-is_bundle", "-views")[:5], many=True).data)


# CATEGORIES VIEW

@api_view(['GET'])
def getAllCategories(request):
    return Response(ServerToClientCategorySerializer(Category.objects.all(), many=True).data)

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
