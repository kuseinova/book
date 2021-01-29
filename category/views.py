from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from category.models import Category
from category.serializers import CategoryAPISerializer


class CategoryApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAPISerializer
