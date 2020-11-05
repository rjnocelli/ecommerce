from inventario_app.models import Order, Product, OrderItem
from rest_framework import serializers
from rest_framework.serializers import CharField, BooleanField, IntegerField


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','views', 'image','description')

# class ServerToClientOrderItemSerializer(serializers.ModelSerializer):
#     class Meta:


# class ServerToClientOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = "__all__"

class OrderItemSerializer(serializers.Serializer):
    id = IntegerField()
    quantity = IntegerField()

    def create(self, validated_data):
        print("SANTI " + str(validated_data))


        return OrderItem(product=validated_data["id"],
                         quantity=validated_data["quantity"])

# Client to server serializer
class OrderSerializer(serializers.Serializer):
    # items =
    items = OrderItemSerializer(many=True)
    complete = BooleanField()
    customer_name = CharField()
    customer_email = CharField()
    # class Meta:
    #     fields = ('id','complete','date_ordered','items','active','customer_name','customer_email')

    def create(self, validated_data):
        order_item_data = validated_data.pop("items")
        order_items = []
        for element in order_item_data:
            order_item = OrderItem(product=Product.objects.get(id = element["id"]),
                                         quantity=element["quantity"])
            order_item.save()
            order_items.append(order_item)
        order = Order.objects.create(**validated_data)
        print("SANTI: " + str(order_items))
        order.items.set(order_items)
        return order

        # order_items = validated_data.pop('items')
        # order_items_array = []
        # for i in order_items:
        #     orderItem = OrderItem.objects.create(quantity = i.quantity, product = i.product)
        #     order_items_array.append(orderItem)
        # print(order_items_array)
        # return Order.objects.create(items = order_items_array, **validated_data)


class JointProductSerializer(serializers.Serializer):
    """
    Joins two serializers together and puts them in a JSON dictionary under
    different keys:
      - most_popular: Holds the most popular products according to their views.
      - all_products: Holds all products.
    """
    most_popular = ProductSerializer(read_only=True, many=True)
    all_products = ProductSerializer(read_only=True, many=True)
