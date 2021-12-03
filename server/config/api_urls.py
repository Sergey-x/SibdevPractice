from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api'
urlpatterns = [
    path('docs/', include('apps.docs.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', include('apps.users.urls')),
    path('transactions/', include('apps.summary.urls')),
    path('widgets/', include('apps.widgets.urls')),
]
