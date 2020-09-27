from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
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


def Index(request):
    products = Product.objects.all()
    featured = products.order_by("-views")[:4]
    return render(request, 'inventario_app/index.html', context={'products': products, 'featured':featured})

class CreateProductView(CreateView):
    template_name = 'inventario_app/create_product.html'
    model = Product
    fields = ['name','price','description','category','image']
    success_url = 'success'


def detail(request, id):
    qs = get_object_or_404(Product, id=id)
    context = {'product': qs}
    return render(request, 'inventario_app/detail_view.html', context)

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
    return render(request, 'inventario_app/checkout.html', context)

def addToCart(request, id):
    item = get_object_or_404(Product, id = id)
    key = 'cart_id'
    if key in request.session:
        session_id = request.session[key] 
        order = get_object_or_404(Order, id = session_id)
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
        return render(request, 'inventario_app/checkout.html',context)
    else:
        order = Order.objects.create()
        request.session[key] = order.id
        orderitem_object = OrderItem.objects.create(product=item)
        order.items.add(orderitem_object)
        context = {"order": order}
        return render(request, 'inventario_app/checkout.html', context)

def cart(request):
    key = 'cart_id'
    try:
        session_id = request.session[key]
        order = get_object_or_404(Order, id=session_id)
        context = {"order": order}
        return render(request, 'inventario_app/checkout.html', context)
    except:
        return HttpResponse('Tu carrito esta vacio')

def email_confirmation(request):
    form = EmailConfirmationForm()
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            session_id = request.session['cart_id'] 
            order = get_object_or_404(Order, id=session_id)
            order_id = urlsafe_base64_encode(force_bytes(order.id))            
            token = order_tokenizer.make_token(order)
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'order_id': order_id,'token': token})
            message = get_template('inventario_app/email_confirmation_message.html').render({
                'confirm_url': url,
                'order': order
            })
            mail = EmailMessage(
                'Dulceria Funes',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                )
            mail.content_subtype = 'html'
            mail.send()
            messages.success(request, f'Se ha enviado un email a esta direccion de correo para confirmar su pedido {email}')
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
          'message': 'Se ha generado un error.',
          'order': order,
          'products': products,
          'featured': featured,
        }

        if order and order_tokenizer.check_token(order, token):
            order.complete = True
            order.save()
            del request.session['cart_id']
            context['message'] = 'Orden confirmada. Uno de nuestros empleados se comunicara con vos via telefono para completar la orden.'

        return render(request, 'inventario_app/index.html', context)


        
    










        
 
        
        



    

    





