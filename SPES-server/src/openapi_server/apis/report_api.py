# coding: utf-8
from typing import Dict, List, Tuple  # noqa: F401

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
    UploadFile,
    File
)
from starlette.responses import FileResponse

from containers import Container
from models.extra_models import TokenModel, GenericNotFoundErrorResponse, \
    GenericUnsupportedMediaTypeResponse, GenericErrorResponse  # noqa: F401
from models.permissio_info import PermissionPartialInfo, PermissionToModify
from models.report_info import ReportInfo, ReportOnlyId
from repositories.repository_exceptions import UploadReportError, FormatReportError, PersonNotFoundError, \
    ReportNotFoundError, PermissionNotFoundError
from security_api import get_token_bearerAuth
from services.permission_service import PermissionService
from services.person_service import PersonService
from services.report_service import ReportService

router = APIRouter()


@router.post(
    "/permissions",
    responses={
        200: {"model": List[ReportOnlyId], "description": "La richiesta dei permessi è stata ricevuta. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["report"],
    summary="Un MED richiede permessi su un sottoinsieme di referti medici.",
)
@inject
async def ask_for_medical_reports_permission(
        request_body: List[ReportOnlyId] = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        permission_service: PermissionService = Depends(Provide[Container.permission_service])
) -> List[ReportOnlyId]:
    """Il medico richiede il permesso alla PF di visualizzare/scaricare referti medici."""
    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role
    try:
        if user_role == "MED" or user_role == "OPS":
            permission_service.add_permission(user_id=user_id, reports_id=request_body)
        else:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print(e.__class__)
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/reports",
    responses={
        200: {"model": List[ReportInfo], "description": "I referti medici sono stati restituiti correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["report"],
    summary="Restituisce i referti medici di una PF.",
)
@inject
async def get_all_medical_reports(
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service]),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> List[ReportInfo]:
    """Restituisce la lista dei referti medici di una PF. Tale richiesta può essere effettuata solamente dalla PF in questione."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role
    pf_id = person_service.get_person_id(user_id=user_id)

    if user_role == "PF":
        try:
            return report_service.get_reports_by_pf_id(pf_id=pf_id)
        except ReportNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get(
    "/reports/pf/{id_pf}",
    responses={
        200: {"model": List[ReportInfo], "description": "I referti medici sono stati restituiti correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["report"],
    summary="Restituisce i referti medici di una PF al medico.",
)
@inject
async def get_all_medical_reports_by_pf_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service])
) -> List[ReportInfo]:
    """Restituisce la lista dei referti medici di una PF. Tale richiesta può essere effettuata solamente dai MED. Se il MED in questione non ha i permessi per un relativo report allora verrà indicato."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "MED" or user_role == 'OPS':
        try:
            return report_service.get_reports_by_user_id_and_pf_id(pf_id=id_pf, user_id=user_id)
        except ReportNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get(
    "/reports/{id_referto}",
    responses={
        200: {"content": {"application/pdf": {}}, "description": "Il referto medico è stato trovato e restituito correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    response_model=UploadFile,
    tags=["report"],
    summary="Trova una referto medico a partire dal suo id.",
)
@inject
async def get_medical_report_by_id(
        id_referto: str = Path(None, description="ID univoco del referto"),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service]),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> FileResponse:
    """Ricerca e restituisce il referto medico con id corrispondente al parametro della richiesta. Tale richiesta può essere effettuata solamente dalla PF."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "PF":
        pf_id = person_service.get_person_id(user_id=user_id)
        try:
            return report_service.get_report_by_owner(pf_id=pf_id, report_id=id_referto)
        except ReportNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif user_role == "MED" or user_role == "OPS":
        try:
            return report_service.get_report(user_id=user_id, report_id=id_referto)
        except ReportNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/permissions",
    responses={
        200: {"model": List[PermissionPartialInfo],
              "description": "La restituzione delle richieste dei permessi è andata a buon fine. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["report"],
    summary="Restituisce le richieste effettuate dai MED.",
)
@inject
async def get_permissions_for_pf(
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),

        permission_service: PermissionService = Depends(Provide[Container.permission_service]),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> List[PermissionPartialInfo]:
    """La PF riceve le richieste relative ai permessi di visualizzazione/download di referti medici effettuate dai MED."""

    pf_id = token_bearerAuth.pf_id
    user_role = token_bearerAuth.role

    if user_role == "PF":
        try:
            return permission_service.get_permissions_in_pending(pf_id=pf_id)
        except PermissionNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.patch(
    "/permissions",
    responses={
        200: {"model": None, "description": "La PF ha concesso/negato l'accesso ai referti medici indicati. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["report"],
    summary="PF concede/nega permessi su un sottoinsieme di referti medici.",
)
@inject
async def set_medical_reports_permissions(
        permissions: List[PermissionToModify] = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        permission_service: PermissionService = Depends(Provide[Container.permission_service]),
        person_service: PersonService = Depends(Provide[Container.person_service])
) -> object:
    """La PF concede/nega accesso ai referti medici nei confronti del medico."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "PF":
        pf_id = person_service.get_person_id(user_id=user_id)
        try:
            permission_service.set_permissions(pf_id=pf_id, permissions=permissions)
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except PermissionNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.post(
    "/reports/upload",
    responses={
        200: {"model": ReportOnlyId, "description": "L'upload del referto medico è andato a buon fine. "},
        400: {"description": "Errore nell'upload. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata(i.e. l'utente che ha effettuato l'upload) non è stata trovata. "},
        415: {"description": "Media type non supportato. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["report"],
    summary="Upload di un referto medico.",
)
@inject
async def upload_medical_report(
        pf_id: str = Form(None, description="ID della PF."),
        title: str = Form(None, description="Titolo referto."),
        referto: UploadFile = File(...),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service])
) -> ReportOnlyId:
    """- Effettua l'upload di un referto medico nel repository della persona fragile. Tale richiesta può essere effettuata solamente dai MED. """

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "MED":
        try:
            return report_service.upload_report(user_id=user_id, pf_id=pf_id, title=title, file=referto)
        except UploadReportError:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        except FormatReportError as err:
            return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            content=GenericUnsupportedMediaTypeResponse(entity_name=err.entity_name,
                                                                        entity_id=err.entity_id).json(),
                            media_type="application/json")
        except PersonNotFoundError as err:
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content=GenericNotFoundErrorResponse(entity_name=err.entity_name,
                                                                 entity_id=err.entity_id).json(),
                            media_type="application/json")
        except Exception as err:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=GenericErrorResponse(description=None, args=None).json(),
                            media_type="application/json")
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

@router.post(
    "/session/reports",
    responses={
        200: {"model": int, "description": "Il MED ha aggiunto correttamente il sottoinsieme specificato alla propria sessione. Si risponde con un intero che indica il numero di oggetti di tipo report presenti nella sessione del MED. ",},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["session"],
    summary="Il MED aggiunge alla propria sessione un sottoinsieme di report.",
)
@inject
async def add_reports_to_session(
        reports: List[ReportOnlyId] = Body(None, description=""),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service])
) -> int:
    """Il MED aggiunge alla propria sessione un sottoinsieme di report."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "MED":
        try:
            return report_service.add_reports_to_session(user_id=user_id, report_ids=reports)
        except Exception as err:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=GenericErrorResponse(description=None, args=None).json(),
                                media_type="application/json")
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

@router.get(
    "/session/reports",
    responses={
        200: {"model": object, "description": "Il MED ha ottenuto la lista dei referti presenti nella propria sessione. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["session"],
    summary="Il MED ottiene dalla propria sessione la lista di referti medici precedentemente selezionati",
)
@inject
async def get_reports_from_session(
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service])
) -> object:
    """Il MED ottiene dalla propria sessione la lista di referti medici precedentemente selezionati."""

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "MED":
        try:
            return report_service.get_reports_from_session(user_id=user_id)
        except ReportNotFoundError as err:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content=GenericNotFoundErrorResponse(entity_name=err.entity_name,
                                entity_id=err.entity_id).json(),
                                media_type="application/json")
        except Exception as err:
            print(err.__class__)
            print(err)
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=GenericErrorResponse(description=None, args=None).json(),
                                media_type="application/json")
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

@router.delete(
    "/session/reports",
    responses={
        200: {"model": object, "description": "Il MED ha eliminato correttamente dalla sessione tutti i referti medici precedentemente selezionati. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["session"],
    summary="Il MED elimina dalla sessione tutti i referti medici precedentemente selezionati. ",
)
@inject
async def empty_reports_from_session(
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service])
) -> object:
    """Il MED elimina dalla sessione tutti i referti medici precedentemente selezionati """

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "MED":
        try:
            return report_service.delete_reports_from_session(user_id=user_id)
        except Exception as err:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=GenericErrorResponse(description=None, args=None).json(),
                                media_type="application/json")
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

@router.delete(
    "/session/reports/{id_referto}",
    responses={
        200: {"model": object, "description": "Il MED ha eliminato dalla sessione il referto medico specificato."},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["session"],
    summary="Il MED elimina dalla sessione il referto medico specificato. ",
)
@inject
async def delete_report_from_session(
        id_referto: str = Path(None, description="ID univoco del referto"),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        report_service: ReportService = Depends(Provide[Container.report_service])
) -> object:
    """Il MED elimina dalla sessione il referto medico specificato. """

    user_id = token_bearerAuth.user_id
    user_role = token_bearerAuth.role

    if user_role == "MED":
        try:
            return report_service.delete_reports_from_session_by_report_id(user_id=user_id, report_id=id_referto)
        except Exception as err:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=GenericErrorResponse(description=None, args=None).json(),
                                media_type="application/json")
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

