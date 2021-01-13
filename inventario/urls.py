import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from inventario_app import views
from inventario_app.views import (
    # ConfirmRegistrationView,
    CreateProductView,
    detail,
    # addToCart,
    # removeFromCart,
    update,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(os.getenv('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('api/', include('api.urls')),
    path('cart/', views.cart, name='cart'),
    path('search/', views.SearchProducts, name='search-view'),
    path('email-confirmation/', views.order_confirmation, name='email-confirmation'),
    # path('confirm-email/<str:order_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm_email'),

    path('create/', views.CreateProductView, name='create'),
    path('admin-product-list', views.AdminProductListView, name='admin-product-list'),
    path('product/<id>/', views.detail, name='detail'),
    # path('product/<id>/add/', views.addToCart, name='add-to-cart'),
    # path('product/<id>/remove/', views.removeFromCart, name='remove-from-cart'),
    path('product/<id>/update/', views.update, name='update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='delete'),

    path('accounts/login/', auth_views.LoginView.as_view()),

    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

