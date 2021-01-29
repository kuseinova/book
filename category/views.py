from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from category.models import Category
from category.serializers import CategoryAPISerializer


class CategoryApiView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategoryAPISerializer
