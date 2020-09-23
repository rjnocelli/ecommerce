from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import Product, OrderItem, Order
from .forms import CreateProductForm
from django.views.generic import FormView, CreateView, DetailView

def Index(request):
    products = Product.objects.all()
    return render(request, 'inventario_app/index.html', context={'products': products})

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
    print(query)
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

# def cart(request):
#    key = 'cart_id'
#     session_id = request.session[key]
#     print(session_id)
#     order = get_object_or_404(Order, id = session_id)
#     context = {"order": order}
#     return render(request, 'inventario_app/checkout.html', context)

    
        
# #         print(order)
#     except:
#         return HttpResponse('Tu carrito esta vacio')

# if key in request.session:

        
    










        
 
        
        



    

    





