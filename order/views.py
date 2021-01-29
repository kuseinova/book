from django.shortcuts import render
from rest_framework import generics, serializers, permissions

from books.models import Book
from order.models import Order, Ordered
from order.serializers import OrderCreateSerializer, OrderDetailSerializer

from rest_framework import generics

class OrderCreateView(generics.ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        elif self.request.method == 'GET':
            return OrderDetailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if len(data.keys()) == 1 and data['ordered']:
            data['user'] = request.user.pk
        if len(data.keys()) == 2:
            ordered = []
            total_price = 0
            if data.get('ordered'):
                for i in data.get('ordered'):
                    if len(i.keys()) == 2:
                        try:
                            book = i['book']
                        except:
                            raise serializers.ValidationError(
                                'Не правильно указана книга')
                        try:
                            quantity = i['quantity']
                        except:
                            raise serializers.ValidationError(
                                'Не правильно указано количество')
                        book = Book.objects.get(pk=book)
                        if book.quantity >= quantity:
                            book.quantity -= quantity
                            book.save()
                        else:
                            raise serializers.ValidationError(
                                "Нету такого количества товара"
                            )
                        obj = Ordered.objects.create(quantity=quantity,
                                                     book=book,
                                                     user=request.user.pk)
                        ordered.append(obj.pk)
                        total_price += quantity * book.price
                    else:
                        raise serializers.ValidationError(
                            'Не правильно переданы данные')
                request.data['ordered'] = ordered
                request.data['total_price'] = total_price
                return self.create(request, *args, **kwargs)
        else:
            raise serializers.ValidationError('Нужно передать три значения')


