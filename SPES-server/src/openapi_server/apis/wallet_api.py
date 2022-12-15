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
    status, UploadFile, File,
)
from pydantic.class_validators import Optional

from models.doc_info import DocInfo, DocPartialInfo
from models.extra_models import TokenModel  # noqa: F401
from repositories.repository_exceptions import UploadDocumentError, FormatReportError, PersonNotFoundError, \
    DocumentNotFoundError
from security_api import get_token_bearerAuth
from services.document_service import DocumentService
from containers import Container
from starlette.responses import FileResponse

router = APIRouter()


@router.put(
    "/wallet/pf/{id_pf}/docs/{doc_id}",
    responses={
        200: {"model": DocPartialInfo,
              "description": "L'aggiornamento del documento specificato è andato a buon fine. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["wallet"],
    summary="Aggiorna il documento identificativo della persona fragile.",
)
@inject
async def update_identification_document_by_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        doc_id: str = Path(None, description="ID univoco del documento identificativo."),
        tipologia: str = Form(None, description="Tipologia di documento"),
        entity: str = Form(None, description="Ente di rilascio."),
        number: str = Form(None, description="Numero del documento."),
        place_of_issue: str = Form(None, description="Luogo di rilascio."),
        release_date: str = Form(None, description="Data di rilascio."),
        expiration_date: str = Form(None, description="Data di scadenza."),
        doc: Optional[List[UploadFile]] = File(None),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        document_service: DocumentService = Depends(Provide[Container.document_service])
) -> DocPartialInfo:
    """- Effettua un aggiornamento del documento indentificativo della PF (chiamata soggetta a rimozione nel caso si volesse mantenere uno storico dei documenti identificativi per tipologia). Tale operazione può essere effettuata solamente dagli OPS. """

    user_id = token_bearerAuth.user_id
    role = token_bearerAuth.role
    if role == "OPS":
        try:
            return document_service.update_document(pf_id=id_pf, upload_by=user_id, doc_id=doc_id, tipologia=tipologia,
                                                    entity=entity, number=number,
                                                    place_of_issue=place_of_issue, release_date=release_date,
                                                    expiration_date=expiration_date,
                                                    files=doc)
        except DocumentNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@router.get(
    "/wallet/pf/{id_pf}/docs/{doc_id}",
    responses={
        200: {"content": {"application/pdf": {}},
              "description": "Il documento specificato è stato restituito correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    response_model=UploadFile,
    tags=["wallet"],
    summary="Restituisce il documento indetificativo della PF in base all'ID.",
)
@inject
async def get_identification_document_by_id(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        doc_id: str = Path(None, description="ID univoco del documento identificativo."),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        document_service: DocumentService = Depends(Provide[Container.document_service])
) -> FileResponse:
    """- Restituisce il documento indetificativo della PF in base all'ID. Tale operazione può essere effettuata solamente dagli OPS e PF."""

    user_id = token_bearerAuth.user_id
    role = token_bearerAuth.role

    try:
        if role == "OPS":
            return document_service.get_document(pf_id=id_pf, doc_id=doc_id)
        elif role == "PF":
            return document_service.get_document_by_user_id(pf_id=id_pf, doc_id=doc_id, user_id=user_id)
        else:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/wallet/pf/{id_pf}/docs",
    responses={
        200: {"model": List[DocInfo], "description": "La lista dei documenti è stata restituita correttamente. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["wallet"],
    summary="Restituisce la lista dei documenti identificativi associati alla PF",
)
@inject
async def get_identification_documents(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        document_service: DocumentService = Depends(Provide[Container.document_service])
) -> List[DocInfo]:
    """- Restituisce la lista dei documenti identificativi associati alla PF. Tale operazione può essere effettuata solamente dagli OPS e PF."""

    user_id = token_bearerAuth.user_id
    role = token_bearerAuth.role

    try:
        if role == "OPS":
            return document_service.get_documents(pf_id=id_pf)
        elif role == "PF":
            return document_service.get_documents_by_user_id(pf_id=id_pf, user_id=user_id)
        else:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    except Exception:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/wallet/pf/{id_pf}/docs/upload",
    responses={
        200: {"model": DocPartialInfo,
              "description": "L'upload del documento identificativo nel portafogli della PF è andato a buon fine. "},
        401: {"description": "Non autorizzato. "},
        403: {"description": "Proibito. "},
        404: {"description": "La risorsa specificata non è stata trovata. "},
        500: {"description": "Internal Server Error. "},
    },
    tags=["wallet"],
    summary="Upload dei documenti identificativi di una PF.",
)
@inject
async def upload_identification_document(
        id_pf: str = Path(None, description="ID univoco della persona fragile"),
        tipologia: str = Form(None, description="Tipologia di documento."),
        entity: str = Form(None, description="Ente di rilascio."),
        number: str = Form(None, description="Numero del documento."),
        place_of_issue: str = Form(None, description="Luogo di rilascio."),
        release_date: str = Form(None, description="Data di rilascio."),
        expiration_date: str = Form(None, description="Data di scadenza."),
        doc: List[UploadFile] = File(...),
        token_bearerAuth: TokenModel = Security(
            get_token_bearerAuth
        ),
        document_service: DocumentService = Depends(Provide[Container.document_service])
) -> DocPartialInfo:
    """- Effettua l'upload di un documento identificativo della persona fragile. Tale operazione può essere effettuata solamente dagli OPS. """

    user_id = token_bearerAuth.user_id
    role = token_bearerAuth.role

    if role == "OPS":
        try:
            return document_service.upload_document(user_id=user_id, pf_id=id_pf, tipologia=tipologia, entity=entity,
                                                    number=number, place_of_issue=place_of_issue,
                                                    release_date=release_date, expiration_date=expiration_date,
                                                    files=doc)
        except UploadDocumentError:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        except FormatReportError:
            return Response(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        except PersonNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except DocumentNotFoundError:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
