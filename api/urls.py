from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api'),
    path('orders/', views.orderList, name='order-list'),

]