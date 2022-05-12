# coding: utf-8

from typing import List
import jwt
from fastapi import Depends, Security  # noqa: F401
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows  # noqa: F401
from fastapi.security import (  # noqa: F401
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery  # noqa: F401

from models.extra_models import TokenModel
from services.user_service import UserService
from containers import Container
from dependency_injector.wiring import inject, Provide


bearer_auth = HTTPBearer()

@inject
def get_token_bearerAuth(credentials: HTTPAuthorizationCredentials = Depends(bearer_auth),
                         user_service: UserService = Depends(Provide[Container.user_service])) -> TokenModel:
    """
    Check and retrieve authentication information from custom bearer token.

    :param credentials Credentials provided by Authorization header
    :type credentials: HTTPAuthorizationCredentials
    :return: Decoded token information or None if token is invalid
    :rtype: TokenModel | None
    """
    pf_id = None
    decoded_token = user_service.check_auth2(token=credentials.credentials)
    print(decoded_token)
    if decoded_token["user_role"] == "PF":
        pf_id = decoded_token["pf_id"]

    token_model = TokenModel(user_id=decoded_token["user_id"],
                             role=decoded_token["user_role"],
                             pf_id=pf_id,
                             expires=decoded_token["expires"])

    return token_model

