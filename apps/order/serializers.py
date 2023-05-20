from rest_framework import serializers
from apps.order.models import OrderItems, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('id', 'product', 'quantity', 'summa')


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'phone', 'address', 'zipcode', 'note', 'order_products', 'get_quantity', 'get_summa')


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('product', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):
    order_products = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'phone', 'address', 'zipcode', 'note', 'order_products')

    def create(self, validated_data):
        order_products = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for item in order_products:
            OrderItems.objects.create(order=order, **item)
        return order
