from datetime import timedelta, datetime

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


# Access token Generator
def _access_token(user):
    access_token = AccessToken.for_user(user)
    access_token['username'] = user.username
    access_token['is_staff'] = user.is_staff
    return str(access_token)


# Refresh token Generator
def _refresh_token(user):
    refresh_token = RefreshToken.for_user(user)
    refresh_token['username'] = user.username
    return str(refresh_token)


# Setting JWTs in cookies
def set_tokens_in_cookie(user):
    response = Response()
    access_expires = datetime.now() + timedelta(minutes=30)
    refresh_expires = datetime.now() + timedelta(days=7)
    response.set_cookie(
        expires=access_expires,
        key='access',
        value=_access_token(user),
        httponly=False,
        secure=True,
        samesite="None"
    )
    response.set_cookie(
        expires=refresh_expires,
        key='refresh',
        value=_refresh_token(user),
        httponly=False,
        secure=True,
        samesite="None"
    )
    return response


# Middleware for checking access tokens
class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ALLOWED_URLS = [
            '/users/login/',
            '/users/signup/',  # URLs without checking
            '/users/refresh/',
        ]

    def __call__(self, request):
        access_token = request.COOKIES.get('access')
        if request.path in self.ALLOWED_URLS:
            return self.get_response(request)
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return self.get_response(request)
