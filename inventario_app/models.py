from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="nombre")
    price = models.DecimalField(max_digits = 5, decimal_places= 2, verbose_name="precio")
    description = models.TextField(max_length=100, verbose_name="descripcion")
    timestamp = models.DateTimeField(default=timezone.now,blank=True, null=True)
    image = models.ImageField(default='chocolate.jpg',blank=True, null=True, verbose_name='imagen')
    category = models.ManyToManyField("Category", verbose_name='categoria', blank=True)
    views = models.IntegerField(default = 0, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='product')
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

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
    active = models.BooleanField(default=True)
    gift = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.items.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total
