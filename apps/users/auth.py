from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from datetime import timedelta


def is_token_expired(token):
    time_elapsed = timezone.now() - token.created
    expiring_time_seconds = 900
    if time_elapsed.total_seconds() > expiring_time_seconds:
        return True
    return False


class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        is_expired = is_token_expired(token)
        if is_expired:
            raise AuthenticationFailed("This Token has expired")
        
        # Extend token expiration
        token.created = timezone.now()
        token.save()

        return (token.user, token)

