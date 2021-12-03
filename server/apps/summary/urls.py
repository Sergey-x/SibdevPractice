from rest_framework import routers

from .viewsets import category, transaction


router = routers.DefaultRouter()
router.register('categories', category.CategoryViewSet, basename='category')
router.register('', transaction.TransactionViewSet, basename='transaction')

app_name = 'summary'

urlpatterns = router.urls
