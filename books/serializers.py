from djoser.serializers import UserSerializer
from rest_framework import serializers

from books.models import Book, Favorites, Ratings
from category.serializers import CategoryBookSerializer


class BookAPISerializer(serializers.ModelSerializer):
    category = CategoryBookSerializer(read_only=True)
    publisher = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            '__all__'
        )


class FavoritesAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('book', 'user')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'
