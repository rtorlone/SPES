"""Repositories module."""

from datetime import date

from contextlib import AbstractContextManager
from sqlite3 import IntegrityError
from typing import Callable, List, Set, Iterator, Dict, Tuple

from sqlalchemy import tuple_
from sqlalchemy.orm import Session, joinedload

from database.report import PersonReport
from database.permission import Permission

from repositories.repository_exceptions import ReportNotFoundError, PermissionNotFoundError, PersonNotFoundError, \
    UserNotFoundError


class ReportRepository:
    """
    Questa classe rappresenta il repository per l'entita Report.
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_reports(self, pf_id: str) -> List[PersonReport]:
        """
        Restituisce una lista di reports. Ciascun report deve far riferimento alla persona fragile in questione.

        :param pf_id: L'id della Persona Fragile.
        :return: Una lista di oggetti PersonReport.
        """

        with self.session_factory() as session:
            reports = session.query(PersonReport).filter(PersonReport.pf_id == pf_id) \
                .options(joinedload(PersonReport.permissions)).all()

            if not reports:
                raise ReportNotFoundError(pf_id)

            return reports

    def get_reports_by_report_ids(self, report_ids: List[str]) -> Iterator[PersonReport]:
        """
        Restituisce una lista di reports medici sulla base di un insieme di id.

        :param report_ids: Id di referti medici,
        :return: Una lista di oggetti PersonReport
        """

        with self.session_factory() as session:
            reports = session.query(PersonReport).filter(PersonReport.id.in_(report_ids)).all()

            if not reports:
                raise ReportNotFoundError(entity_id=None)

            return reports

    def get_report(self, user_id: str, report_id: str) -> PersonReport:
        """
        Restituisce un referto medico sulla base dell'id. Il referto è restituto solamente se lo user possiede i permessi.

        :param user_id:
        :param report_id: id del referto medico.
        :return: Un oggetto PersonReport
        """

        with self.session_factory() as session:
            report = session.query(Permission).filter(
                (Permission.user_id == user_id) & (Permission.document_id == report_id) & (Permission.permission)) \
                .from_self(PersonReport).join(Permission.document).first()

            if not report:
                raise ReportNotFoundError(entity_id=report_id)

            return report

    def get_report_pf_id_and_report_id(self, pf_id: str, report_id: str) -> PersonReport:
        """
        Restituisce un referto medico sulla base della persona fragile e del report_id.

        :param pf_id: L'id della persona fragile.
        :param report_id: L'id del referto medico.
        :return: Un oggetto PersonReport.
        """

        with self.session_factory() as session:
            report = session.query(PersonReport).filter(
                (PersonReport.pf_id == pf_id) & (PersonReport.id == report_id)).first()

            if not report:
                raise ReportNotFoundError(entity_id=report_id)

            return report

    def insert_report(self, user_id: str, pf_id: str, report_id: str, title: str, upload_date: date,
                      path: str) -> PersonReport:
        """
        Inserisce nel repository i metadati relativi ad un report medico.

        :param title:
        :param report_id:
        :param pf_id:
        :param user_id:
        :param upload_date:
        :param path:
        :return: Un oggetto di tipo PersonReport
        """

        with self.session_factory() as session:
            report = PersonReport(id=report_id,
                                  pf_id=pf_id,
                                  title=title,
                                  upload_by=user_id,
                                  upload_date=upload_date,
                                  path=path)
            session.add(report)
            session.commit()
            session.refresh(report)
            return report

    def get_permissions_in_pending_by_pf_id(self, pf_id: str) -> List[Permission]:
        """
        Restituisce una lista di oggetti Permission relativi alla persona fragile in questione. Tali oggetti devono avere valore di pending pari a true.

        :param pf_id: id della PF.
        :return: Una lista di oggetti Permission.
        """
        with self.session_factory() as session:

            permissions = session.query(PersonReport).from_self(Permission).join(PersonReport.permissions).filter(PersonReport.pf_id == pf_id).filter(Permission.pending == True).all()

            if not permissions:
                raise PermissionNotFoundError(entity_id=None)

            return permissions

    def get_permissions(self, pf_id: str) -> Iterator[Permission]:
        """
        Restituisce una lista di oggetti Permission relativi alla persona fragile in questione.

        :param pf_id: id della PF.
        :return: Una lista di oggetti Permission.
        """
        with self.session_factory() as session:
            permissions = session.query(Permission).filter(PersonReport.pf_id == pf_id) \
                .from_self(Permission).join(Permission.document).all()

            if not permissions:
                raise PermissionNotFoundError(pf_id)

            return permissions

    def get_permissions_with_filter(self, user_id: str, pending: bool = None, permission: bool = None) -> Iterator[
        Permission]:
        """
        Restituisce una lista di oggetti Permission, filtrata per peding e permission.

        :param permission:
        :param pending:
        :param user_id: id dello user che possiede tali permessi.
        :return: Una lista di oggetti Permission.
        """
        with self.session_factory() as session:
            query = session.query(Permission).filter(
                (Permission.user_id == user_id))

            if permission is not None:
                query = query.filter(Permission.permission == permission)

            if pending is not None:
                query = query.filter(Permission.pending == pending)

            permissions = query.options(joinedload(Permission.document)).all()

            if not permissions:
                raise PermissionNotFoundError(user_id)

            return permissions

    def add_permissions(self, user_id: str, reports_id: List[str], date: date) -> Permission:
        """
        Aggiunge una richiesta di permessi per uno specifico report nel repository.

        :param reports_id:
        :param date:
        :param user_id: L'id dello user che richiede il permesso.
        :return: Un oggetto di tipo Permission
        """

        if not reports_id:
            return

        with self.session_factory() as session:
            for report_id in reports_id:
                permission = Permission(user_id=user_id,
                                        document_id=report_id,
                                        created=date,
                                        pending=True,
                                        permission=False)
                session.add(permission)
            try:
                session.commit()
            except IntegrityError as err:
                if "pf_id" in str(err.orig):
                    raise UserNotFoundError(entity_id=user_id)
                if "document_id" in str(err.orig):
                    raise ReportNotFoundError(entity_id=report_id)
            return permission

    def add_existing_permission(self, user_id: str, reports_id: List[int], date: date) -> Iterator[Permission]:
        """
        Aggiunge i report indicati nella lista dei permessi in pending. Prerequisito fondamentale è che tali entry già esistono.

        :param user_id:
        :param reports_id:
        :param date:
        :return:
        """
        with self.session_factory() as session:
            permissions = session.query(Permission).filter(
                (Permission.user_id == user_id) & (Permission.document_id.in_(reports_id))).all()

            if not permissions:
                return

            for permission in permissions:
                permission.pending = True
                permission.created = date

            session.commit()

            return permissions

    def get_existing_permissions(self, user_id: str, reports_id: Set[int]) -> Iterator[Permission]:
        """
        Restituisce una lista di permessi in base agli id passati.

        :param user_id:
        :param reports_id: lista di id di report.
        :return: Una lista di oggetti di tipo Permission
        """

        with self.session_factory() as session:
            permissions = session.query(Permission).filter((Permission.user_id == user_id) &
                                                           (Permission.document_id.in_(reports_id))).all()
            if not permissions:
                PermissionNotFoundError(entity_id=None)

            return permissions

    def get_existing_permissions_reports_ids(self, user_id: str, reports_id: Set[int]) -> Set[int]:
        """
        Fa la stessa cosa della funzione precedente con la differenza che qui si restituiscono i report id.

        :param user_id:
        :param reports_id:
        :return: Un insieme di report id.
        """

        permissions = self.get_existing_permissions(user_id=user_id, reports_id=reports_id)
        list_of_reports = set()

        for permission in permissions:
            list_of_reports.add(permission.document_id)

        return list_of_reports

    def set_permissions(self, pf_id: str, permissions_to_value: Dict[Tuple[str, str], bool]) -> None:
        """
        Imposta i valori dei permessi per il sottoinsieme indicato.

        :param pf_id:
        :param permissions_to_value:
        :return: None.
        """

        with self.session_factory() as session:
            permissions = session.query(Permission).from_self(Permission).join(Permission.document).filter(
                (PersonReport.pf_id == pf_id) & (Permission.pending == True) &
                (tuple_(Permission.user_id, Permission.document_id).in_(permissions_to_value.keys()))) \
                .all()

            if not permissions:
                raise PermissionNotFoundError(entity_id=None)

            for permission in permissions:
                permission.permission = permissions_to_value[(permission.user_id, permission.document_id)]
                permission.pending = False
            session.commit()
