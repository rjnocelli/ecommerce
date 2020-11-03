from inventario_app.models import Order, Product, OrderItem
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','views', 'image')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ('id','quantity','date_added','product')

class OrderSerializer(serializers.ModelSerializer):
    # items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','complete','date_ordered','items','active','customer_name','customer_email')
        depth = 3

    # def create(self, validated_data):
    #     print(validated_data)
    #     # order_items = validated_data.pop('items')
    #     # print(order_items)
    # #     print(validated_data)
    # #     order_items_array = []
    # #     # for i in order_items:
    # #     #     orderItem = OrderItem.objects.create(quantity = i.quantity, product = i.product)
    # #     #     order_items_array.append(orderItem)
    # #     # print(order_items_array)
    # #     order = Order.objects.create(items = order_items_array, **validated_data)
    #     return validated_data

class JointProductSerializer(serializers.Serializer):
    """
    Joins two serializers together and puts them in a JSON dictionary under
    different keys:
      - most_popular: Holds the most popular products according to their views.
      - all_products: Holds all products.
    """
    most_popular = ProductSerializer(read_only=True, many=True)
    all_products = ProductSerializer(read_only=True, many=True)
