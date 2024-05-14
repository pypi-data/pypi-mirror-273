import time

import jwt

from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from jsm_user_services.drf_tools.exceptions import InvalidToken as CustomInvalidToken
from jsm_user_services.drf_tools.exceptions import NotAuthenticated as CustomNotAuthenticated
from jsm_user_services.services.user import current_jwt_token
from jsm_user_services.support.auth_jwt import get_decoded_oauth_token


class JWTBearerAuthentication(authentication.BaseAuthentication):
    ALGORITHM_HS256 = "HS256"
    ALGORITHM_RS256 = "RS256"

    def __init__(self):
        self.hs256_authentication = JWTTokenUserAuthentication()

    def authenticate(self, request):
        token = current_jwt_token()
        if token is None:
            raise CustomNotAuthenticated()

        try:
            header = jwt.get_unverified_header(token)
        except jwt.DecodeError:
            raise CustomInvalidToken()

        alg = header.get("alg")

        authentication_methods = {
            self.ALGORITHM_HS256: lambda: self.is_hs256_alg_token_valid(request),
            self.ALGORITHM_RS256: lambda: (AnonymousUser(), token) if self.is_rs256_alg_token_valid(token) else None,
        }

        if alg is None or alg not in authentication_methods:
            raise CustomInvalidToken()

        authenticate_method = authentication_methods[alg]()

        if authenticate_method is None:
            raise CustomInvalidToken()

        return authenticate_method

    def is_rs256_alg_token_valid(self, token: str) -> bool:
        try:
            payload = get_decoded_oauth_token(token)
            current_timestamp = int(time.time())
            is_token_expired = "exp" in payload and current_timestamp > payload["exp"]
            is_sub_claim_in_payload = "sub" in payload
            if not is_token_expired and is_sub_claim_in_payload:
                return True
        except jwt.DecodeError:
            return False
        return False

    def is_hs256_alg_token_valid(self, request):
        try:
            return self.hs256_authentication.authenticate(request)
        except InvalidToken:
            raise CustomInvalidToken()
        except NotAuthenticated:
            raise CustomNotAuthenticated()


class OauthJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = current_jwt_token()
        if token is None:
            raise CustomNotAuthenticated()

        try:
            payload = get_decoded_oauth_token(token)
            current_timestamp = int(time.time())
            is_token_expired = "exp" in payload and current_timestamp > payload["exp"]
            is_sub_claim_in_payload = "sub" in payload
            if not is_token_expired and is_sub_claim_in_payload:
                return (AnonymousUser(), token)
            else:
                raise CustomInvalidToken()
        except jwt.DecodeError:
            raise CustomInvalidToken()
