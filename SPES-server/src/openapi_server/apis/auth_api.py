# coding: utf-8

from typing import Dict, List  # noqa: F401

from dependency_injector.wiring import inject, Provide
from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from containers import Container
from models.extra_models import TokenModel  # noqa: F401
from models.login import Login
from models.login import LoginResponse
from repositories.repository_exceptions import UserNotFoundError
from services.user_service import UserService

router = APIRouter()


@router.post(
    "/auth",
    responses={
        200: {"model": LoginResponse, "description": "L'utente è stato autenticato correttamente. "},
        401: {"description": "Non autorizzato. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["auth"],
    summary="Autentica l'utente nel sistema.",
)
@inject
async def auth(login: Login = Body(None, description=""),
              user_service: UserService = Depends(Provide[Container.user_service])) -> LoginResponse:
    """Autentica l'utente nel sistema."""
    try:
        encoded_token, first_access = user_service.auth(username=login.username, password=login.password)
        response = LoginResponse()
        response.jwt = encoded_token["access_token"]
        response.expires_at = user_service.get_expires_auth(encoded_token["access_token"])
        response.first_access = first_access

        return response
    except UserNotFoundError:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


