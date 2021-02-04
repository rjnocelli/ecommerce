import os

from dotenv import load_dotenv
load_dotenv()

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api.views import getProductsOnSearch
from inventario_app.views import (Index,
    cart, order_confirmation, CreateProductView,
    AdminProductListView, detail, update, ProductDelete)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path(os.getenv('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path('', Index, name='index'),
    path('api/', include('api.urls')),
    path('cart/', cart, name='cart'),
    path('email-confirmation/', order_confirmation, name='email-confirmation'),
    path('search/', getProductsOnSearch, name='search'),
    path('create/', CreateProductView, name='create'),
    path('admin-product-list', AdminProductListView, name='admin-product-list'),
    path('product/<id>/', detail, name='detail'),
    path('product/<id>/update/', update, name='update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='delete'),
    path('accounts/login/', auth_views.LoginView.as_view()),

    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

