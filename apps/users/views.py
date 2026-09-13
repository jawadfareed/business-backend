from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.users.selectors import user_list_active, user_get_by_id
from apps.users.services import user_create, user_update
from apps.users.serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer, CustomTokenObtainPairSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view returning user payload and custom claims.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = CustomTokenObtainPairSerializer


class UserListCreateApi(APIView):
    """
    API view to list active users (GET) or create a new user (POST).
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        users = user_list_active()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(**serializer.validated_data)
        output_serializer = UserSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class UserDetailApi(APIView):
    """
    API view to retrieve or update a user detail.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = user_get_by_id(user_id=user_id)
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, user_id):
        user = user_get_by_id(user_id=user_id)
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = user_update(user=user, **serializer.validated_data)
        output_serializer = UserSerializer(updated_user)
        return Response(output_serializer.data)


class UserMeApi(APIView):
    """
    API view to get or update current logged in user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = user_update(user=request.user, **serializer.validated_data)
        return Response(UserSerializer(updated_user).data)
