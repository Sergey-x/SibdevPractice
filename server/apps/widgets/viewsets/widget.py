from rest_framework import permissions, viewsets

from ..models.widget import Widget
from ..serializers import widget as serializers


class WidgetViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create` and `destroy` actions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializers_matching = {
            'create': serializers.CreateWidgetSerializer,
            'list': serializers.ListWidgetSerializer,
            'destroy': serializers.DestroyWidgetSerializer,
        }
        return serializers_matching[self.action]

    def get_queryset(self):
        return Widget.objects.filter(owner=self.request.user)
