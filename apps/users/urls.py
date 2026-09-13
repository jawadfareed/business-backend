from django.urls import path
from apps.users.views import UserListCreateApi, UserDetailApi, UserMeApi

app_name = 'users'

urlpatterns = [
    path('', UserListCreateApi.as_view(), name='list-create'),
    path('me/', UserMeApi.as_view(), name='me'),
    path('<int:user_id>/', UserDetailApi.as_view(), name='detail'),
]
