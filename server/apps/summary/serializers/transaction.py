from rest_framework import serializers

from ..models.transaction import Transaction


class BaseTransactionSerializer(serializers.ModelSerializer):
    """
    Base serializer for Transaction model.
    Other transaction serializers must be inherited from it.
    """

    class Meta:
        model = Transaction
        fields = ('category', 'sum')


class CreateTransactionSerializer(BaseTransactionSerializer):
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return Transaction.objects.create(**validated_data)

    def validate_category(self, value):
        """
        Checks that the category belongs to the current-user.
        """
        current_user = self.context.get('request').user
        error_msg = (
            f"Недопустимый первичный ключ \"{value.id}\" - объект не существует."
        )
        if value.owner != current_user:
            raise serializers.ValidationError(detail=error_msg)
        return value


class UpdateTransactionSerializer(CreateTransactionSerializer):
    pass


class ListTransactionSerializer(BaseTransactionSerializer):
    category_type = serializers.CharField(read_only=True)

    class Meta(BaseTransactionSerializer.Meta):
        fields = ('category', 'sum', 'id', 'category_type', 'owner')


class DestroyTransactionSerializer(BaseTransactionSerializer):
    pass
