from rest_framework import serializers
from .models import Order, Ordered


class OrderedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordered
        fields = ('book', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'user', 'ordered', 'total_price'
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    ordered = OrderedCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'user', 'total_price', 'ordered', 'created_at'
        )
