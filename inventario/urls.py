from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from inventario_app import views
from inventario_app.views import ConfirmRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('product/', include('inventario_app.urls')),
    path('cart/', views.cart, name='cart'),
    path('search/', views.SearchProducts, name='search-view'),
    path('email-confirmation/', views.email_confirmation, name='email-confirmation'),
    path('confirm-email/<str:order_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm_email')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
