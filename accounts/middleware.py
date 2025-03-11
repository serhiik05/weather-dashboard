from requests import Request
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class BlacklistMiddleware(MiddlewareMixin):

    """Middleware to block blacklisted JWT tokens."""

    def process_request(self, request: Request) -> JsonResponse:
        auth_header = request.headers.get("Authorization", None)
        if auth_header and auth_header.startswith("Bearer "):
            token_str = auth_header.split(" ")[1]
            try:
                token = AccessToken(token_str)
                if BlacklistedToken.objects.filter(token__jti=token["jti"]).exists():
                    return JsonResponse({"error": "Token is blacklisted."}, status=401)
            except Exception:
                return JsonResponse({"error": "Invalid token."}, status=401)
