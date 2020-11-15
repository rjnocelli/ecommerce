from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from inventario_app import views
from inventario_app.views import (
    ConfirmRegistrationView,
    CreateProductView,
    detail,
    addToCart,
    removeFromCart,
    update,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('api/', include('api.urls')),
    path('cart/', views.cart, name='cart'),
    path('search/', views.SearchProducts, name='search-view'),
    path('email-confirmation/', views.email_confirmation, name='email-confirmation'),
    path('confirm-email/<str:order_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm_email'),

    path('create/', CreateProductView.as_view(), name='create'),
    path('admin-product-list', views.AdminProductListView, name='admin-product-list'),
    path('product/<id>/', views.detail, name='detail'),
    path('product/<id>/add/', views.addToCart, name='add-to-cart'),
    path('product/<id>/remove/', views.removeFromCart, name='remove-from-cart'),
    path('product/<id>/update/', views.update, name='update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='delete'),

    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
