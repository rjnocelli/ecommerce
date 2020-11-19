from django.conf import settings
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages

from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import order_tokenizer
from django.template.loader import get_template
from django.core.mail import EmailMessage

from .models import Product, OrderItem, Order
from .forms import CreateProductForm, EmailConfirmationForm
from django.views.generic import FormView, CreateView, DetailView, View, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.decorators.csrf import csrf_exempt

from api import serializers

def Index(request):
    return render(request, 'inventario_app/index.html')

# Admin UI Views

@login_required
def CreateProductView(request):
    form = CreateProductForm()
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Se ha agregado un nuevo producto a la base de datos')
            return HttpResponseRedirect(reverse('index'))
    return render(request, "inventario_app/admin_create_product.html", context = {"form": form})

class ProductDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'inventario_app/admin_delete_confirmation.html'
    model = Product
    success_url = reverse_lazy('index')

@login_required
def AdminProductListView(request):
    products = Product.objects.all()
    return render(request, 'inventario_app/admin_product_list.html', {'products': products})

def detail(request, id):
    qs = get_object_or_404(Product, id=id)
    context = {'product': qs}
    return render(request, 'inventario_app/detail_view.html', context)

@login_required
def update(request, id):
    qs = get_object_or_404(Product, id=id)
    form = CreateProductForm(instance = qs)
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES, instance = qs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, "inventario_app/update_product.html", context = {"form": form, "product":qs})

def SearchProducts(request):
    queryset = Product.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    context = {
        'products': queryset
    }
    return render(request, 'inventario_app/search_results.html', context)

def removeFromCart(request, id):
    item = get_object_or_404(Product, id = id)
    key = 'cart_id'
    if key in request.session:
        session_id = request.session[key]
        order = get_object_or_404(Order, id = session_id)
        if order.items.filter(product__id = item.id).exists():
            orderitem_object = order.items.filter(product__id = item.id)[0]
            orderitem_object.quantity -= 1
            orderitem_object.save()
    context = {'order':order}
    return HttpResponseRedirect(reverse('cart'))

def cart(request):
    return render(request, 'inventario_app/checkout.html')

@csrf_exempt
def order_confirmation(request):
    form = EmailConfirmationForm()
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["order_items"]:
                order_items = []
                for element in form.cleaned_data["order_items"]:
                    order_item = OrderItem(
                        product=Product.objects.get(id = element["id"]),
                        quantity=element["quantity"])
                    order_item.save()
                    order_items.append(order_item)
                customer_name = f"{form.cleaned_data['name']} {form.cleaned_data['surname']}"
                order = Order.objects.create(
                    customer_name=customer_name,
                    customer_email=form.cleaned_data["email"],
                    customer_phone_number=form.cleaned_data["phone_number"],
                    gift=form.cleaned_data['gift'])
                order.items.set(order_items)
                order.save()   
                message = get_template('inventario_app/email_confirmation_shop.html').render({
                    'order': order,
                })
                mail = EmailMessage(
                    'Dulceria Funes',
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    )
                mail.content_subtype = 'html'
                mail.send()
                if form.cleaned_data['email']:         
                    customer_email = form.cleaned_data['email']
                    message = get_template('inventario_app/email_confirmation_customer.html').render({
                        'order': order,
                    })
                    mail = EmailMessage(
                        'Dulceria Funes',
                        message,
                        settings.EMAIL_HOST_USER,
                        [customer_email],
                        )
                    mail.content_subtype = 'html'
                    mail.send()
                messages.info(request, 'Orden enviada. Nos contactaremos con usted para ultimar detalles del pedido.')
                request.session['order_complete'] = True
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, 'No puede enviar una orden vacia.')
            return render(request, 'inventario_app/index.html')
    context = {"form": form}
    return render(request, 'inventario_app/email_confirmation.html', context)

# def addToCart(request, id):
#     item = get_object_or_404(Product, id = id)
#     try:
#         order = Order.objects.get(active=True)
#         if order.items.filter(product__id = item.id).exists():
#             orderitem_object = order.items.filter(product__id = item.id)[0]
#             orderitem_object.quantity += 1
#             orderitem_object.save()
#         else:
#             orderitem_object = OrderItem.objects.create(product=item)
#             orderitem_object.product.views += 1
#             orderitem_object.product.save()
#             order.items.add(orderitem_object)
#         context = {"order": order}
#     except:
#         order = Order.objects.create(active=True)
#         orderitem_object = OrderItem.objects.create(product=item)
#         order.items.add(orderitem_object)
#         context = {"order": order}
#     return HttpResponseRedirect(reverse('cart'))

# class ConfirmRegistrationView(View):
#     def get(self, request, order_id, token):
#         order_id = force_text(urlsafe_base64_decode(order_id))
#         order = Order.objects.get(id=order_id)

#         if order and order_tokenizer.check_token(order, token):
#             order.complete = True
#             order.active = False
#             order.save()
#             message = get_template('inventario_app/email_confirmation_final.html').render({
#                 'order': order,
#             })
#             mail = EmailMessage(
#                 'Dulceria Funes',
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [settings.EMAIL_HOST_USER],
#                 )
#             mail.content_subtype = 'html'
#             mail.send()
#             messages.success(request, 'Orden confirmada. Uno de nuestros empleados se comunicara con usted via telefono para definir detalles de pago.')
#         else:
#             messages.error(request, 'Ha ocurrido un problema con el link. Por favor intentelo de nuevo.')
#         return render(request, 'inventario_app/index.html')

# def add_to_cart(request, id):
#     item = get_object_or_404(Product, id = id)
#     key = 'cart_id'
#     if key in request.session:
#         session_id = request.session[key]
#         order = get_object_or_404(Order, id = session_id)
#         if order.items.filter(product__id = item.id).exists():
#             orderitem_object = order.items.filter(product__id = item.id)[0]
#             orderitem_object.quantity += 1
#             orderitem_object.save()
#         else:
#             orderitem_object = OrderItem.objects.create(product=item)
#             orderitem_object.product.views += 1
#             orderitem_object.product.save()
#             order.items.add(orderitem_object)
#         context = {"order": order}
#     else:
#         order = Order.objects.create(active=True)
#         request.session[key] = order.id
#         orderitem_object = OrderItem.objects.create(product=item)
#         order.items.add(orderitem_object)
#         context = {"order": order}
#     return HttpResponseRedirect(reverse('cart'))






# @csrf_exempt
# def email_confirmation(request):
#     form = EmailConfirmationForm()
#     if request.method == 'POST':
#         form = EmailConfirmationForm(request.POST)
#         if form.is_valid():
#             order_items = []
#             for element in form.cleaned_data["order_items"]:
#                 order_item = OrderItem(
#                     product=Product.objects.get(id = element["id"]),
#                     quantity=element["quantity"])
#                 order_item.save()
#                 order_items.append(order_item)
#             customer_name = f"{form.cleaned_data['name']} {form.cleaned_data['surname']}"
#             order = Order.objects.create(
#                 customer_name=customer_name,
#                 customer_email=form.cleaned_data["email"],
#                 customer_phone_number=form.cleaned_data["phone_number"],
#                 gift=form.cleaned_data['gift'])
#             order.items.set(order_items)
#             order.save()            
#             customer_email = form.cleaned_data['email']
#             order_id = urlsafe_base64_encode(force_bytes(order.id))
#             token = order_tokenizer.make_token(order)
#             url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'order_id': order_id,'token': token})
#             message = get_template('inventario_app/email_confirmation_link.html').render({
#                 'confirm_url': url,
#                 'order': order,
#             })
#             mail = EmailMessage(
#                 'Dulceria Funes',
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [customer_email],
#                 )
#             mail.content_subtype = 'html'
#             mail.send()
#             messages.info(request, f'Se ha enviado un email a esta direccion de correo para confirmar su pedido {form.cleaned_data["email"]}')
#             return render(request, 'inventario_app/index.html', {'order_sent': True})
#     context = {"form": form}
#     return render(request, 'inventario_app/email_confirmation.html', context)