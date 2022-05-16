# coding: utf-8

from typing import Dict, List  # noqa: F401

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

from models.address import Address
from models.citizenship import Citizenship
from models.extra_models import TokenModel  # noqa: F401
from models.marital_status import MaritalStatus
from models.pf_info import PfInfo, PfInfoWithIds, PFPartialInfoWithIds, PfInfoWithIdsForUpdate
from models.pf_info import PfId
from models.user_info import UserInfoForUpdate, UserInfoWithPwd
from repositories.repository_exceptions import UserNotFoundError
from security_api import get_token_bearerAuth
from services.person_service import PersonService
from repositories.person_repository import PersonNotFoundError
from containers import Container
from dependency_injector.wiring import inject, Provide

from services.user_service import UserService
from services.email_service import EmailService

router = APIRouter()


@router.get(
    "/pf/{id_pf}",
    responses={
        200: {"model": PfInfoWithIds, "description": "I dettagli anagrafici della PF sono stati restituiti correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Ottiene i dati anagrafici di una PF a partire dal suo id.",
)
@inject
async def get_pf_info_by_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> PfInfoWithIds:

    """Ottiene i dati anagrafici di una PF a partire dal suo id."""

    user_role = token_bearerAuth.role

    if user_role in ["OPS", "PF"]:
        try:
            pf_info = person_service.get_person(id_pf)
            return pf_info
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        Response(status_code=status.HTTP_403_FORBIDDEN)


@router.patch(
    "/user/pf",
    responses={
        200: {"model": UserInfoWithPwd, "description": "Le credenziali dello user sono state cambiate correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Aggiorna lo user corrispondente alla PF specificata.",
)
@inject
async def update_pf_user_info(
        user_info: UserInfoForUpdate = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        userService: UserService = Depends(Provide[Container.user_service])
) -> PfInfoWithIds:

    """Aggiorna lo user corrispondente alla PF specificata."""

    user_role = token_bearerAuth.role

    if user_role in ["PF"]:
        pf_id = token_bearerAuth.pf_id

        try:
            return userService.update_user(pf_id=pf_id, old_pwd=user_info.old_pwd, new_pwd=user_info.new_pwd)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)



@router.post(
    "/pf",
    responses={
        201: {"model": PfId, "description": "La registrazione della PF è andata a buon fine. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Registra una PF nel sistema.",
)
@inject
async def register_pf(
        pf_info: PfInfo = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service]),
        email_service: EmailService = Depends(Provide[Container.email_service])

) -> str:
    """- Effettua la registrazione di una PFnel sistema, inserendo i suoi dati anagrafici. Tale registrazione può essere effettuata solamente dagli OPS. """

    user_id = token_bearerAuth.user_id
    role = token_bearerAuth.role

    if role == "OPS":
        pf_info = person_service.create_person(user_id, pf_info)
        await email_service.send_credentials(dest=pf_info.email, username=pf_info.username, password=pf_info.password)
        return Response(status_code=status.HTTP_201_CREATED, content=pf_info.json(), media_type="aplication/json")
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get(
    "/search/pf",
    responses={
        200: {"model": List[PFPartialInfoWithIds], "description": "È stata restituita una lista di PF. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Restituisce una lista di PF in base alla query sottomessa.",
)
@inject
async def search_pfs_by_query(
        firstname: str = Query(None, description="Il nome della persona fragile."),
        lastname: str = Query(None, description="Il cognome della persona fragile."),
        nicknames: str = Query(None, description="Il nickname della persona fragile."),
        cf: str = Query(None, description="Il codice fiscale della persona fragile."),
        is_anonymous: bool = Query(None, description="La persona fragile è anonima?"),
        is_foreign: bool = Query(None, description="La persona fragile è straniera?"),
        is_dead: bool = Query(None, description="La persona fragile è morta?"),
        verified: bool = Query(None, description="La persona fragile è stata verificata?"),
        offset: int = Query(0, description="Offset della ricerca."),
        limit: int = Query(10, description="Limit della ricerca."),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> List[PFPartialInfoWithIds]:

    """Effettua una ricerca della PF sottoponendo al sistema una query. Tale ricerca può essere effettuata da OPS e MED."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    return person_service.get_persons_by_query(firstname=firstname, lastname=lastname, nicknames=nicknames,
                                               cf=cf,
                                               is_anonymous=is_anonymous, is_foreign=is_foreign,
                                               is_dead=is_dead, verified=verified, offset=offset, limit=limit)

    if user_role in ["OPS", "MED"]:
        try:
            return person_service.get_persons_by_query(firstname=firstname, lastname=lastname, nicknames=nicknames,
                                                       cf=cf,
                                                       is_anonymous=is_anonymous, is_foreign=is_foreign,
                                                       is_dead=is_dead, verified=verified, offset=offset, limit=limit)
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.patch(
    "/pf/{id_pf}",
    responses={
        200: {"model": object, "description": "I dettagli anagrafici della PF sono stati modificati correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Aggiorna i dati anagrafici di una PF a partire dal suo ID.",
)
@inject
async def update_pf_info_by_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        pf_info: PfInfoWithIdsForUpdate = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> object:
    """Aggiorna i dati anagrafici di una PF a partire dal suo ID. Tale operazione può essere effettuata solamente dagli OPS."""
    user_id = token_bearerAuth.user_id
    return person_service.update_person(user_id=user_id, pf_id=id_pf, item=pf_info)


@router.post(
    "/pf/{id_pf}/citizenship",
    responses={
        200: {"model": object, "description": "I dettagli anagrafici relativi alle cittadinanze della PF sono stati modificati correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Aggiorna i dati relativi alle cittadinanze della PF specificata",
)
@inject
async def add_citizenship_by_pf_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        pf_info: List[Citizenship] = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> object:

    """Aggiorna i dati relativi alle cittadinanze della PF specificata. Tale operazione può essere effettuata solamente dagli OPS."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "OPS":
        try:
            return person_service.add_citizenship_by_pf_id(user_id=user_id, pf_id=id_pf, items=pf_info)
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except UserNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.post(
    "/pf/{id_pf}/marital_status",
    responses={
        200: {"model": object, "description": "I dettagli anagrafici della PF relativi agli stati civili sono stati modificati correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Aggiorna i dati relativi agli stati civili della PF specificata.",
)
@inject
async def add_marital_status_by_pf_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        pf_info: List[MaritalStatus] = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> object:

    """Aggiorna i dati relativi agli stati civili della PF specificata. Tale operazione può essere effettuata solamente dagli OPS."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "OPS":
        try:
            return person_service.add_marital_status_by_pf_id(user_id=user_id, pf_id=id_pf, items=pf_info)
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except UserNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.post(
    "/pf/{id_pf}/address",
    responses={
        200: {"model": object, "description": "I dettagli anagrafici relativi agli indirizzi della PF sono stati modificati correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["pf"],
    summary="Aggiorna i dati relativi agli indirizzi della PF specificata.",
)
@inject
async def add_address_by_pf_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        pf_info: List[Address] = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> object:

    """Aggiorna i dati relativi agli indirizzi della PF specificata. Tale operazione può essere effettuata solamente dagli OPS."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "OPS":
        try:
            return person_service.add_address_by_pf_id(user_id=user_id, pf_id=id_pf, items=pf_info)
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except UserNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
