from datetime import timedelta

from rest_framework import serializers

from ..models.widget import Widget


class BaseWidgetSerializer(serializers.ModelSerializer):
    """
    This is the base serializer class for Widget model.
    Other widget serializers must be inherited from it.
    """

    class Meta:
        model = Widget
        fields = (
            'id',
            'category',
            'limit',
            'duration',
            'criteria',
            'color',
            'creation_date',
        )


class CreateWidgetSerializer(BaseWidgetSerializer):
    color = serializers.CharField(max_length=10)

    def validate_duration(self, value: timedelta):
        """
        Check that duration is acceptable quantity of days.
        """
        if value.days not in Widget.VALID_DURATION:
            raise serializers.ValidationError(
                f"You can chose only this day-periods {Widget.VALID_DURATION}."
            )
        return timedelta(days=value.days)

    def validate_color(self, value):
        """
        Check that color specified in hex correctly.
        """
        if value.startswith('0x'):
            return value[2:]
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return Widget.objects.create(**validated_data)


class DestroyWidgetSerializer(BaseWidgetSerializer):
    pass


class ListWidgetSerializer(BaseWidgetSerializer):
    class Meta(BaseWidgetSerializer.Meta):
        fields = (
            'id',
            'category',
            'limit',
            'duration',
            'criteria',
            'color',
            'creation_date',
            'ending_date',
            'sum',
            'owner',
        )
