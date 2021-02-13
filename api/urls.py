from django.urls import path
from . import views
from rest_framework import routers



urlpatterns = [
    path('', views.apiOverview, name='api'),
    path('order-list/', views.getAllOrders, name='order-list'),
    path('order-detail/<str:pk>/', views.orderDetail, name='order-detail'),
    path('order-update/<str:pk>/', views.orderUpdate, name='order-update'),
    path('order-delete/<str:pk>/', views.orderDelete, name='order-delete'),

    path('product-list/', views.getAllProducts, name='product-list'),
    path('popular-products/', views.getMostPopularProducts, name='popular-products'),
    path('product-infinite/', views.infinte_scroll_view.as_view(), name='product-infinite'),
    path('categories-list/', views.getAllCategories, name='cat-list')

]

