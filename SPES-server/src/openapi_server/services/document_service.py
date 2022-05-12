"""Services module."""

import os
import uuid
from datetime import date
from typing import List

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError

from models.doc_info import DocInfo, DocPartialInfo
from repositories.document_repository import DocumentRepository
from repositories.repository_exceptions import FormatReportError, DocumentNotFoundError, \
    UploadDocumentError


class DocumentService:
    """
    Questa classe definisce i servizi relativi all'entità Document
    """

    BASE_PATH = "../../documents/"
    SUPPORTED_MEDIA_TYPE = ["application/pdf"]

    def __init__(self, document_repository: DocumentRepository) -> None:
        self._repository: DocumentRepository = document_repository

    def get_documents(self, pf_id: str) -> List[DocInfo]:
        """
        Restituisce una lista di documenti amministrativi a partire dall'id della persona fragile.

        :param pf_id: L'id della persona fragile.
        :return: Una lista di oggetti DocPartialInfo
        """
        documents = self._repository.get_documents(pf_id=pf_id)
        docs_info = []
        for document in documents:
            doc_info = DocInfo(id=document.id,
                               tipologia=document.tipologia,
                               upload_date=document.upload_date,
                               entity=document.entity,
                               number=document.number,
                               place_of_issue=document.place_of_issue,
                               release_date=document.release_date,
                               expiration_date=document.expiration_date)
            docs_info.append(doc_info)
        return docs_info

    def get_documents_by_user_id(self, pf_id: str, user_id: str):
        """
        Restituisce una lista di documenti amministrativi solo se quest'ultimi sono posseduti dallo user.

        :param pf_id: L'id della persona fragile.
        :param user_id: L'id dello user.
        :return: Una lista di oggetti DocPartialInfo
        """
        documents = self._repository.get_documents_by_user_id(pf_id=pf_id, user_id=user_id)
        docs_info = []
        for document in documents:
            doc_info = DocInfo(id=document.id,
                               tipologia=document.tipologia,
                               upload_date=document.upload_date,
                               entity=document.entity,
                               number=document.number,
                               place_of_issue=document.place_of_issue,
                               release_date=document.release_date,
                               expiration_date=document.expiration_date)
            docs_info.append(doc_info)
        return docs_info

    def get_document(self, pf_id: str, doc_id: str) -> FileResponse:
        """
        Restituisce un documento amministrativo.

        :param pf_id: L'id della persona fragile.
        :param doc_id: L'id del documento.
        :return: Un oggetto di tipo FileResponse
        """
        document = self._repository.get_document(pf_id=pf_id, doc_id=doc_id)

        headers = {"id": document.id, "entity": document.entity, "tipologia": document.tipologia,
                   "place_of_issue": document.place_of_issue,
                   "release_date": str(document.release_date), "expiration_date": str(document.expiration_date),
                   "upload_date": str(document.upload_date), "number": str(document.number)}
        report_response = FileResponse(document.path, headers=headers, media_type="application/pdf")

        return report_response

    def get_document_by_user_id(self, pf_id: str, doc_id: str, user_id: str) -> FileResponse:
        """
        Restituisce un documento amministrativo solo se lo user lo possiede.

        :param user_id: L'id dello user.
        :param pf_id: L'id della persona fragile.
        :param doc_id: L'id del documento.
        :return: Un oggetto di tipo FileResponse
        """
        document = self._repository.get_document_by_user_id(pf_id=pf_id, doc_id=doc_id, user_id=user_id)

        headers = {"id": document.id, "entity": document.entity, "tipologia": document.tipologia,
                   "place_of_issue": document.place_of_issue,
                   "release_date": str(document.release_date), "expiration_date": str(document.expiration_date),
                   "upload_date": str(document.upload_date), "number": str(document.number)}
        report_response = FileResponse(document.path, headers=headers)

        return report_response

    def upload_document(self, user_id: str, pf_id: str, tipologia: str, entity: str, number: str, place_of_issue: str,
                        release_date: date, expiration_date: date, file: UploadFile) -> DocPartialInfo:
        """
        Salva il report sul filesystem del server e i relativi metadati nel repository.

        :param expiration_date:
        :param release_date:
        :param place_of_issue:
        :param number:
        :param entity:
        :param tipologia:
        :param user_id:
        :param pf_id
        :param file:
        :return:
        """
        doc_id = str(uuid.uuid4())
        file_path = self.BASE_PATH + doc_id + ".pdf"
        contents = file.file.read()

        if file.content_type not in self.SUPPORTED_MEDIA_TYPE:
            raise FormatReportError(entity_id=doc_id, media_type=file.content_type)

        # Salva su filesystem
        with open(file_path, 'wb') as f:
            f.write(contents)
            f.close()

        today = date.today()

        # Salva i metadati sul repository
        try:
            self._repository.insert_document(upload_by=user_id, pf_id=pf_id, doc_id=doc_id, tipologia=tipologia,
                                             entity=entity,
                                             number=number, place_of_issue=place_of_issue,
                                             release_date=release_date, expiration_date=expiration_date,
                                             upload_date=today,
                                             path=file_path)
            return DocPartialInfo(id=doc_id, tipologia=tipologia, upload_date=today)
        except IntegrityError:
            os.remove(file_path)
            raise DocumentNotFoundError(entity_id=doc_id)
        except Exception:
            os.remove(file_path)
            raise UploadDocumentError(entity_id=doc_id)

    def update_document(self, upload_by: str, pf_id: str, doc_id: str, tipologia: str, entity: str, number: str,
                        place_of_issue: str, release_date: date, expiration_date: date,
                        file: UploadFile) -> DocPartialInfo:
        """
        Aggiorna il documento, salvando il nuovo file nel filesystem e aggiornando i metadati del repository.

        :param upload_by: 
        :param pf_id: 
        :param doc_id: 
        :param tipologia: 
        :param entity: 
        :param number: 
        :param place_of_issue: 
        :param release_date: 
        :param expiration_date: 
        :param upload_date: 
        :param file: 
        :return: 
        """
        file_path = self.BASE_PATH + doc_id + ".pdf"

        # Salva su filesystem (sovrascrive)
        if file:
            contents = file.file.read()
            with open(file_path, 'wb') as f:
                f.write(contents)
                f.close()

        today = date.today()

        # Salva i metadati sul repository
        try:
            self._repository.update_document(upload_by=upload_by, pf_id=pf_id, doc_id=doc_id, tipologia=tipologia,
                                             entity=entity, number=number, place_of_issue=place_of_issue,
                                             release_date=release_date,
                                             expiration_date=expiration_date, upload_date=today, path=file_path)
            return DocPartialInfo(id=doc_id, tipologia=tipologia, upload_date=today)
        except IntegrityError:
            os.remove(file_path)
            raise DocumentNotFoundError(entity_id=doc_id)
        except Exception:
            os.remove(file_path)
            raise UploadDocumentError(entity_id=doc_id)
