from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api'),
    path('order-list/', views.orderList, name='order-list'),
    path('order-detail/<str:pk>/', views.orderDetail, name='order-detail'),
    path('order-create/', views.orderCreate, name='order-create'),
    path('order-update/<str:pk>/', views.orderUpdate, name='order-update'),

]