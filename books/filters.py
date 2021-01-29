from django_filters import rest_framework as filters

from .models import Book


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookFilter(filters.FilterSet):

    class Meta:
        model = Book
        fields = ['category',]