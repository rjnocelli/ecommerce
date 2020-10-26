from django.urls import path
from . import views
from rest_framework import routers



urlpatterns = [
    path('', views.apiOverview, name='api'),
    path('order-list/', views.getActiveOrder, name='order-list'),
    path('order-detail/<str:pk>/', views.orderDetail, name='order-detail'),
    path('order-create/', views.orderCreate, name='order-create'),
    path('order-update/<str:pk>/', views.orderUpdate, name='order-update'),
    path('order-delete/<str:pk>/', views.orderDelete, name='order-delete'),

    path('product-list/', views.getAllProducts, name='product-list'),
    path('popular-products/', views.getMostPopularProducts, name='popular-products'),
    
]

