from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from inventario_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('product/', include('inventario_app.urls')),
    path('cart/', views.cart, name='cart'),
    path('search/', views.SearchProducts, name='search-view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
