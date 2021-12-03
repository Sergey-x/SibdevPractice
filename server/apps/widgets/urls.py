from rest_framework import routers

from .viewsets.widget import WidgetViewSet


app_name = 'widgets'

router = routers.DefaultRouter()
router.register('', WidgetViewSet, basename='widgets')

urlpatterns = router.urls
