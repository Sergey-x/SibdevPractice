from rest_framework import serializers

from ..models.transaction import Transaction


class DatePeriodSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    income = serializers.SerializerMethodField()
    expense = serializers.SerializerMethodField()

    def create(self, validated_data=None):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def validate(self, data):
        """
        Check begin of date-interval is less than end.
        """
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                "Specified incorrect datetime period."
            )
        data['owner'] = self.context['request'].user.id
        return data

    class Meta:
        fields = ('start_date', 'end_date', 'income', 'expense')

    def get_income(self, obj):
        return Transaction.objects.income_sum_for_period(**self.validated_data)

    def get_expense(self, obj):
        return Transaction.objects.expense_sum_for_period(**self.validated_data)
