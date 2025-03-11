from drf_spectacular.utils import extend_schema
from requests import Request
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


@extend_schema(
    description="Register a new user with a username, email, password, and optional role.",
    request=RegisterSerializer,
    responses={201: UserSerializer, 400: {"description": "Validation error"}},
)
class RegisterView(generics.CreateAPIView):
    """Register a new user."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    description="Login a user and return access & refresh JWT tokens.",
    request=LoginSerializer,
    responses={200: LoginSerializer, 400: {"description": "Invalid credentials"}},
)
class LoginView(APIView):
    """Login a user and return JWT tokens."""

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


@extend_schema(
    description="Logout the user by blacklisting their refresh token.",
    request={"type": "object", "properties": {"refresh": {"type": "string"}}},
    responses={200: {"description": "Successfully logged out."}, 400: {"description": "Invalid token."}},
)
class LogoutView(APIView):
    """Logout a user by blacklisting their refresh token."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."})
        except Exception as e:
            return Response({"error": "Invalid token."}, status=400)


@extend_schema(
    description="Retrieve the authenticated user's profile information.",
    responses={200: UserSerializer, 401: {"description": "Unauthorized"}},
)
class ProfileView(generics.RetrieveAPIView):
    """Get user profile (requires authentication)."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user
