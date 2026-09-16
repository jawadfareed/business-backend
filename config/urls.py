from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from apps.users.views import CustomTokenObtainPairView


def health_check(request):
    return JsonResponse({"status": "ok", "message": "Business Tracker Backend API is operational."})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/v1/users/', include('apps.users.urls', namespace='users_v1')),
]
