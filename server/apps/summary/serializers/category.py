from rest_framework import serializers

from ..models.category import Category


class BaseCategorySerializer(serializers.ModelSerializer):
    """
    Base serializer for Category model.
    Other transaction serializers must be inherited from it.
    """

    class Meta:
        model = Category
        fields = ('title', 'type')


class CreateCategorySerializer(BaseCategorySerializer):
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return Category.objects.create(**validated_data)


class ListCategorySerializer(BaseCategorySerializer):
    sum = serializers.IntegerField(read_only=True)

    class Meta(BaseCategorySerializer.Meta):
        fields = ('title', 'type', 'id', 'sum', 'owner')


class DestroyCategorySerializer(BaseCategorySerializer):
    pass
