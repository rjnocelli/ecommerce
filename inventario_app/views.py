from django.conf import settings

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
from django.views.generic import FormView, CreateView, DetailView, View

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


def Index(request):
    products = Product.objects.all()
    featured = products.order_by("-views")[:4]
    return render(request, 'inventario_app/index.html', context={'products': products, 'featured':featured})

class CreateProductView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'inventario_app/create_product.html'
    model = Product
    fields = ['name','price','description','category','image']
    success_url = reverse_lazy('index')
    success_message = f'Has agregado un nuevo producto a la base de datos'

def detail(request, id):
    qs = get_object_or_404(Product, id=id)
    context = {'product': qs}
    return render(request, 'inventario_app/detail_view.html', context)

@login_required
def update(request, id):
    qs = get_object_or_404(Product, id=id)
    form = CreateProductForm(instance = qs)
    if request.method == "POST":
        form = CreateProductForm(request.POST, instance = qs)
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
    
def Success(request):
    return render(request, 'inventario_app/success.html')

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

def addToCart(request, id):
    item = get_object_or_404(Product, id = id)
    try:
        order = Order.objects.get(active=True)
        if order.items.filter(product__id = item.id).exists():
            orderitem_object = order.items.filter(product__id = item.id)[0]
            orderitem_object.quantity += 1
            orderitem_object.save()
        else:
            orderitem_object = OrderItem.objects.create(product=item)
            orderitem_object.product.views += 1
            orderitem_object.product.save()
            order.items.add(orderitem_object)
        context = {"order": order}
    except:
        order = Order.objects.create(active=True)
        orderitem_object = OrderItem.objects.create(product=item)
        order.items.add(orderitem_object)
        context = {"order": order}
    return HttpResponseRedirect(reverse('cart'))

        
def cart(request):
    try:
        order = Order.objects.get(active=True)
        context = {"order": order}
        return render(request, 'inventario_app/checkout.html', context)
    except:
        messages.warning(request,'No tienes una orden abierta. Necesitas agregar el primer producto para abrir una orden.')
        products = Product.objects.all()
        featured = products.order_by("-views")[:4]
        context = {
            'products': products,
            'featured': featured,
        }
        return render(request, 'inventario_app/index.html', context)

def email_confirmation(request):
    form = EmailConfirmationForm()
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            session_id = request.session['cart_id']
            customer_info = form.cleaned_data
            customer_email = customer_info['email']
            request.session['customer_info'] = customer_info
            order = get_object_or_404(Order, id=session_id)
            order_id = urlsafe_base64_encode(force_bytes(order.id))            
            token = order_tokenizer.make_token(order)
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'order_id': order_id,'token': token})
            message = get_template('inventario_app/email_confirmation_link.html').render({
                'confirm_url': url,
                'order': order,
                'customer_info': customer_info
            })
            mail = EmailMessage(
                'Dulceria Funes',
                message,
                settings.EMAIL_HOST_USER,
                [customer_email],
                )
            mail.content_subtype = 'html'
            mail.send()
            messages.info(request, f'Se ha enviado un email a esta direccion de correo para confirmar su pedido {customer_email}')
            return HttpResponseRedirect(reverse('index'))
    context = {"form": form}
    return render(request, 'inventario_app/email_confirmation.html', context)

class ConfirmRegistrationView(View):
    def get(self, request, order_id, token):
        products = Product.objects.all()
        featured = products.order_by("-views")[:4]
        order_id = force_text(urlsafe_base64_decode(order_id))
        
        order = Order.objects.get(id=order_id)
    
        context = {
          'order': order,
          'products': products,
          'featured': featured,
        }

        if order and order_tokenizer.check_token(order, token):
            customer_info = request.session['customer_info']
            order.complete = True
            order.save()
            message = get_template('inventario_app/email_confirmation_final.html').render({
                'order': order,
                'customer_info': customer_info,  
            })
            mail = EmailMessage(
                'Dulceria Funes',
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                )
            mail.content_subtype = 'html'
            mail.send()
            del request.session['cart_id'], request.session['customer_info']
            messages.success(request, 'Orden confirmada. Uno de nuestros empleados se comunicara con usted via telefono para definir detalles de pago.')
        else: 
            messages.error(request, 'Ha ocurrido un problema con el link. Por favor intentelo de nuevo.')
        return render(request, 'inventario_app/index.html', context)


def checkOut(request):
    return render(request, 'inventario_app/checkout.html')
        
 
        
        



    

    





