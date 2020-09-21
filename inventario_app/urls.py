from django.urls import path, include
from inventario_app import views
from inventario_app.views import CreateProductView


urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create'),
    path('create/success/', views.Success, name='success'),
    path('<id>/', views.detail, name='detail'),
    path('search/', views.SearchProducts, name='search-view'),
    path('<id>/add/', views.addToCart, name='add-to-cart'),
]
