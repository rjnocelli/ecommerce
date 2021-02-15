from inventario_app.models import Order, Product, OrderItem, Category
from rest_framework import serializers
from rest_framework.serializers import CharField, BooleanField, IntegerField

class ServerToClientCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = Category
        fields = "__all__"

class ServerToClientProductSerializer(serializers.ModelSerializer):
    category = ServerToClientCategorySerializer(many=True)
    class Meta:
        model = Product
        fields = "__all__"

class ServerToClientProductSerializerOnSearch(serializers.ModelSerializer):
    category = ServerToClientCategorySerializer(many=True)
    class Meta:
        model = Product
        fields = "__all__"

class ServerToClientOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 2

class ServerToClientOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = 'quantity'

#    ----------------------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id'

class OrderItemSerializer(serializers.Serializer):
    id = IntegerField()
    quantity = IntegerField()

    def create(self, validated_data):
        return OrderItem(product=validated_data["id"],
                         quantity=validated_data["quantity"])

# Client to server serializer
class OrderSerializer(serializers.Serializer):
   
    items = OrderItemSerializer(many=True)
    complete = BooleanField()
    customer_name = CharField()
    customer_email = CharField()
    
    def create(self, validated_data):
        order_item_data = validated_data.pop("items")
        order_items = []
        for element in order_item_data:
            order_item = OrderItem(product=Product.objects.get(id = element["id"]),
                                         quantity=element["quantity"])
            order_item.save()
            order_items.append(order_item)
        order = Order.objects.create(**validated_data)
        order.items.set(order_items)
        return order

class JointProductSerializer(serializers.Serializer):
    """
    Joins two serializers together and puts them in a JSON dictionary under
    different keys:
      - most_popular: Holds the most popular products according to their views.
      - all_products: Holds all products.
    """
    most_popular = ServerToClientOrderSerializer(read_only=True, many=True)
    all_products = ServerToClientOrderSerializer(read_only=True, many=True)
