from rest_framework import serializers

from category.models import Category


class CategoryAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'title',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategoryAPISerializer(
                instance.children.all(), many=True
            ).data
        return representation


class CategoryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'title',
        )
