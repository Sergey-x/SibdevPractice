from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..filters import DateIntervalFilter
from ..models.transaction import Transaction
from ..serializers import transaction as serializers
from ..serializers.common import DatePeriodSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `update` and `destroy` actions.
    """
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = DateIntervalFilter

    def get_serializer_class(self):
        serializers_matching = {
            'create': serializers.CreateTransactionSerializer,
            'update': serializers.UpdateTransactionSerializer,
            'partial_update': serializers.UpdateTransactionSerializer,
            'list': serializers.ListTransactionSerializer,
            'destroy': serializers.DestroyTransactionSerializer,
            'get_period_report': DatePeriodSerializer,
        }
        return serializers_matching[self.action]

    def get_queryset(self):
        """
        Return personal transactions filtered by date period.
        """
        queryset = Transaction.objects.filter(owner=self.request.user)
        queryset = self.filter_queryset(queryset=queryset)
        return queryset

    @action(detail=False, url_path='period-info', methods=('get',))
    def get_period_report(self, request):
        """
        Return income and expense sums by date period.
        """
        serializer = self.get_serializer(data=self.request.query_params)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
