
from .authorization_header_auth import AuthorizationHeaderSession
from .environment import DRF_AUTH_TOKEN_VARIABLE


class DjangoTokenAuthSession(AuthorizationHeaderSession):
    """
    API Session with django rest framework token authentication
    """
    session_type = 'token'
    token_name = 'Token'
    token_var = DRF_AUTH_TOKEN_VARIABLE
