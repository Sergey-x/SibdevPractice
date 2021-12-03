from rest_framework import serializers

from .models import CustomUser


class BaseCustomUserSerializer(serializers.ModelSerializer):
    """
    Base serializer for CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'id')


class CreateCustomUserSerializer(BaseCustomUserSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta(BaseCustomUserSerializer.Meta):
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        new_user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
