from djoser.serializers import UserSerializer
from rest_framework import serializers

from books.models import Book, Favorites, Ratings, Comment
from category.serializers import CategoryBookSerializer, CategoryAPISerializer


class BookAPISerializer(serializers.ModelSerializer):
    category = CategoryBookSerializer(read_only=True)
    publisher = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'



class FavoritesAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorites
        fields = ('book', 'user')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['image'] = self._get_image_url(instance)
    #     representation['categories'] = CategoryAPISerializer(instance.categories.all(), many=True).data
    #     representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
    #     return representation
