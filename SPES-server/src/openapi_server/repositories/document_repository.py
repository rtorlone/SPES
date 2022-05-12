"""Repositories module."""

from datetime import date

from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from database.document import PersonDocument
from database.person import Person

from repositories.repository_exceptions import ReportNotFoundError, PermissionNotFoundError, DocumentNotFoundError, \
    PersonNotFoundError, UserNotFoundError


class DocumentRepository:
    """
    Questa classe rappresenta il repository per l'entita Document.
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_documents(self, pf_id: str) -> List[PersonDocument]:
        """
        Restituisce una lista di documents. Ciascun document deve avere come owner il pf_id.
        :param pf_id: L'id della Persona Fragile.
        :return: Una lista di oggetti PersonDocument.
        """

        with self.session_factory() as session:
            documents = session.query(PersonDocument).filter(PersonDocument.pf_id == pf_id).all()
            if not documents:
                raise PersonNotFoundError(entity_id=pf_id)

            return documents

    def get_documents_by_user_id(self, pf_id: str, user_id: str) -> List[PersonDocument]:
        """
        Restituisce una lista di documents. Ciascun document deve appartenere allo user.
        :param pf_id: L'id della persona fragile.
        :param user_id: L'id dello user.
        :return: Una lista di oggetti PersonDocument.
        """
        with self.session_factory() as session:
            documents = session.query(PersonDocument).filter(
                (PersonDocument.pf_id == pf_id) & (Person.user_id == user_id)) \
                .from_self(PersonDocument).join(PersonDocument.person).all()
            if not documents:
                raise UserNotFoundError(entity_id=user_id)

            return documents

    def get_document(self, pf_id: str, doc_id: str) -> PersonDocument:
        """
        Restituisce un document a partire dal suo id.
        :param pf_id: L'id della persona fragile.
        :param doc_id: L'id del document.
        :return: Un oggetto di tipo PersonDocument.
        """

        with self.session_factory() as session:
            document = session.query(PersonDocument).filter((PersonDocument.id == doc_id) & (PersonDocument.pf_id == pf_id)).first()

            if not document:
                raise DocumentNotFoundError(doc_id)

            return document

    def get_document_by_user_id(self, doc_id:str, pf_id: str, user_id: str) -> PersonDocument:
        """
        Restituisce un document a partire dal suo id. Condizione necessaria: lo user deve possedere tale document.
        :param pf_id: L'id della persona fragile.
        :param user_id: L'id dello user.
        :param doc_id: L'id del document.
        :return: Un oggetto di tipo PersonDocument.
        """

        with self.session_factory() as session:
            document = session.query(PersonDocument).filter(
                (PersonDocument.id == doc_id) & (PersonDocument.pf_id == pf_id) & (Person.user_id == user_id)). \
                from_self(PersonDocument).join(PersonDocument.person).first()

            if not document:
                raise DocumentNotFoundError(doc_id)

            return document

    def insert_document(self, upload_by: str, pf_id: str, doc_id: str, tipologia: str, entity: str, number: str,
                        place_of_issue: str, release_date: date, expiration_date: date, upload_date: date, path: str) -> PersonDocument:
        """
        Inserisce nel repository i metadati relativi al documento.
        :param number:
        :param upload_by:
        :param pf_id:
        :param doc_id:
        :param tipologia:
        :param entity:
        :param place_of_issue:
        :param release_date:
        :param expiration_date:
        :param upload_date:
        :param path:
        :return:
        """

        with self.session_factory() as session:
            document = PersonDocument(id=doc_id,
                                      pf_id=pf_id,
                                      upload_by=upload_by,
                                      tipologia=tipologia,
                                      entity=entity,
                                      number=number,
                                      place_of_issue=place_of_issue,
                                      release_date=release_date,
                                      expiration_date=expiration_date,
                                      upload_date=upload_date,
                                      path=path)
            session.add(document)
            session.commit()
            session.refresh(document)
            return document

    def update_document(self, upload_by: str, pf_id: str, doc_id: str, tipologia: str, entity: str, number: str,
                        place_of_issue: str, release_date: date, expiration_date: date, upload_date: date, path: str):
        """
        Esegue l'update del document.
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
        :param path:
        :return: Un oggetto di tipo PersonDocument
        """
        with self.session_factory() as session:
            document = session.query(PersonDocument).filter((PersonDocument.id == doc_id) & (PersonDocument.pf_id == pf_id)).first()

            if not document:
                raise DocumentNotFoundError(doc_id)

            document.upload_by = upload_by
            document.entity = entity
            document.number = number
            document.tipologia = tipologia
            document.place_of_issue = place_of_issue
            document.release_date = release_date
            document.expiration_date = expiration_date
            document.upload_date = upload_date
            document.path = path

            session.commit()
            session.refresh(document)

            return document
