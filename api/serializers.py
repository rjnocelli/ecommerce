from inventario_app.models import Order, Product, OrderItem
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id','name','price','views', 'image')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id','quantity','date_added','product')

class OrderSerializer(serializers.ModelSerializer):
    # order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('id','complete','date_ordered','items','active')
        depth = 2