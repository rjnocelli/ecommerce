from django.urls import path
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'product-list', views.productList2, 'Products')



urlpatterns = [
    path('', views.apiOverview, name='api'),
    path('order-list/', views.getActiveOrder, name='order-list'),
    path('order-detail/<str:pk>/', views.orderDetail, name='order-detail'),
    path('order-create/', views.orderCreate, name='order-create'),
    path('order-update/<str:pk>/', views.orderUpdate, name='order-update'),
    path('order-delete/<str:pk>/', views.orderDelete, name='order-delete'),

    path('popular-products', views.getMostPopularProducts, name='popular-products')
]

urlpatterns += router.urls