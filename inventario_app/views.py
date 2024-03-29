from django.conf import settings
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
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

from api.serializers import ProductSerializer


def Index(request):
    return render(request, 'inventario_app/index.html')

def Contact(request):
    return render(request, 'inventario_app/contact.html')

def serve_search_template(request):
    query = request.GET.get('q')
    return render(request, "inventario_app/search_results.html", context={"q":query})

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
    products = Product.objects.all().order_by('name')
    return render(request, 'inventario_app/admin_product_list.html', {'products': products})

def detail(request, id):    
    qs = get_object_or_404(Product, id=id)
    product_data = {
        "id": qs.id,
        "name": qs.name,
        "price": qs.price,
        "sold_by_weight": qs.sold_by_weight,
        "price_100g": qs.price_100g,
        "price_200g": qs.price_200g,
        "price_300g": qs.price_300g,
    }
    mydata = qs.id
    context = {'product': qs, 'product_data': product_data}
    if qs.sold_by_weight:
        context['sold_by_weight'] = [("100g",qs.price_100g),("200g",qs.price_200g),("300g",qs.price_300g)]
    return render(request, 'inventario_app/detail_view.html', context)

@login_required
def update(request, id):
    qs = get_object_or_404(Product, id=id)
    form = CreateProductForm(instance = qs)
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES, instance = qs)
        if form.is_valid():
            if form.cleaned_data['sold_by_weight']:
                form.cleaned_data['price'] = None
            form.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, "inventario_app/update_product.html", context = {"form": form, "product":qs})

# def SearchProducts(request):
#     queryset = Product.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(name__icontains=query) |
#             Q(description__icontains=query) |
#             Q(category__name__icontains=query)
#         ).distinct()
#     context = {
#         'products': queryset
#     }
#     return render(request, 'inventario_app/search_results.html', context)

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
    return render(request, 'inventario_app/cart.html')

@csrf_exempt
def order_confirmation(request):
    form = EmailConfirmationForm()
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["order_items"]:
                order_items = []
                for element in form.cleaned_data["order_items"]:
                    product = Product.objects.get(id = element["id"])
                    if element["sold_by_weight"] == False:
                        order_item = OrderItem(
                            product = product,
                            product_name=element["product_name"],
                            quantity=element["quantity"],
                            product_price = product.price)
                        order_item.save()
                        order_items.append(order_item) 
                    else:
                        weight_price = element["sold_by_weight"].split()[1]
                        order_item = OrderItem(
                            product_name=element["product_name"],
                            product=product,
                            quantity=element["quantity"],
                            sold_by_weight_info=weight_price)
                        if weight_price == '100g':
                            order_item.product_price = product.price_100g
                        elif weight_price == '200g':
                            order_item.product_price = product.price_200g
                        elif weight_price == '300g':
                            order_item.product_price = product.price_300g
                        order_item.save()
                        order_items.append(order_item)
                customer_name = f"{form.cleaned_data['name']} {form.cleaned_data['surname']}"
                order = Order(
                    customer_name=customer_name,
                    customer_email=form.cleaned_data["email"],
                    customer_phone_number=form.cleaned_data["phone_number"],
                    customer_location=form.cleaned_data["location"],
                    customer_address=form.cleaned_data["customer_address"],
                    gift=form.cleaned_data['gift'])
                order_items_total = sum(item.product_price * item.quantity for item in order_items)
                if order_items_total < 1000:
                    # fields valid but order less than minimum
                        for item in order_items:
                            item.delete()
                        messages.warning(request, 'La compra mínima es de $1000 más el envío.')
                        return redirect('/?q=failed')
                order.save()
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
                request.session['order_completed'] = True
                request.session.set_expiry(1)
                order.save()
                messages.success(request, 'Orden enviada. Nos contactaremos con usted para ultimar detalles del pedido.')
                return redirect('/?q=success')
            else:          
                # reCAPTCHA valid but order empty 
                # creates a new order on the client side from scratch
                request.session['order_failed'] = True
                request.session.set_expiry(1)
                messages.warning(request, 'No puede enviar una orden vacia.')
                return redirect('/?q=failed')
        else:
            # at least one of the fields is not valid (empty order items or failed reCAPTCHA)
            messages.warning(request, 'reCAPTCHA incorrecto u orden vacía, inténtelo de nuevo.')
            return redirect('/?q=failed')
    context = {"form": form}
    return render(request, 'inventario_app/email_confirmation.html', context)
