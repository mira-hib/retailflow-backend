from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class BindingJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None

        user, token = user_auth_tuple
        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        if token.get('ip') != ip or token.get('user_agent') != user_agent:
            raise AuthenticationFailed('Token utilisé depuis un autre contexte !')

        return user, token