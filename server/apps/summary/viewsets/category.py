from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..filters import DateIntervalFilterForCategory
from ..models.category import Category
from ..serializers import category as serializers


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create` and `destroy` actions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializers_matching = {
            'create': serializers.CreateCategorySerializer,
            'list': serializers.ListCategorySerializer,
            'destroy': serializers.DestroyCategorySerializer,
            'get_category_sum': serializers.ListCategorySerializer,
        }
        return serializers_matching[self.action]

    def get_queryset(self):
        """
        Return queryset with only personal categories.
        """
        return Category.objects.filter(owner=self.request.user)

    @action(detail=False, url_path='info', methods=('get',))
    def get_category_sum(self, request):
        """
        Return category collection with sum of bound transactions.
        """
        categories = DateIntervalFilterForCategory(
            self.request.query_params,
            queryset=self.get_queryset(),
        ).qs
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
