from django.db import models
from django.utils import timezone

class Product(models.Model):

    choices = (
        ('100g', 0),
        ('200g', 0),
        ('300g', 0),
    )

    name = models.CharField(max_length=50, verbose_name="nombre")
    price = models.DecimalField(max_digits = 6, decimal_places= 2, verbose_name="precio", null=True, blank=True)
    sold_by_weight = models.BooleanField(default = False, verbose_name= 'Producto Vendido x Peso')
    price_100g = models.DecimalField(max_digits = 6, decimal_places= 2, verbose_name="precio por 100g", null=True, blank=True)
    price_200g = models.DecimalField(max_digits = 6, decimal_places= 2, verbose_name="precio por 200g", null=True, blank=True)
    price_300g = models.DecimalField(max_digits = 6, decimal_places= 2, verbose_name="precio por 300g", null=True, blank=True)
    description = models.TextField(max_length=400, verbose_name="descripcion", null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now,blank=True, null=True)
    image = models.ImageField(default='chocolate.jpg',blank=True, null=True, verbose_name='imagen')
    category = models.ManyToManyField("Category", verbose_name='categoria', blank=True)
    views = models.IntegerField(default = 0, null=True, blank=True)
    is_bundle = models.BooleanField(default = False, verbose_name='Es Promocion')
    in_stock = models.BooleanField(default = True, verbose_name='En Stock')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Categorias')

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='product')
    product_name = models.CharField(max_length=50, null=True, blank=True)
    product_price = models.DecimalField(max_digits = 6, decimal_places= 2, null=True, blank=True)
    sold_by_weight_info = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    @property
    def add(self):
        self.quantity += 1
    @property
    def take(self):
        self.quantity += 1

class Order(models.Model):
    items = models.ManyToManyField("OrderItem", related_name='products')
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    customer_name = models.CharField(max_length=100, blank=True)
    customer_email = models.CharField(max_length=100, blank=True)
    customer_phone_number = models.CharField(max_length=100, blank=True)
    customer_location = models.CharField(max_length=100, blank=True)
    customer_address = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    gift = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.items.all()
        for i in orderitems:
            print(i.product_name, type(i.product_price))
        total = sum([item.product_price * item.quantity for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total


