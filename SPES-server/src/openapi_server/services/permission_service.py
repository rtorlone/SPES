"""Services module."""

from datetime import date
from typing import List

from models.permissio_info import PermissionPartialInfo, PermissionToModify
from models.report_info import ReportOnlyId
from repositories.report_repository import ReportRepository


class PermissionService:
    """
    Questa classe definisce i servizi relativi all'entità Permission
    """

    def __init__(self, report_repository: ReportRepository) -> None:
        self._repository: ReportRepository = report_repository

    def add_permission(self, user_id: str, reports_id: List[ReportOnlyId]) -> None:
        """
        Aggiunge i permessi
        :param user_id: L'id dello user che fa richiesta dei permessi
        :param reports_id: La lista dei report a cui chiedere i permessi.
        :return:
        """
        list_of_reports_id = set()
        for item in reports_id:
            list_of_reports_id.add(str(item.report_id))

        today = date.today()

        existing_report_ids_with_permission = self._repository.get_existing_permissions_reports_ids(user_id=user_id,
                                                                                                    reports_id=list_of_reports_id)

        # Faccio la differenza per aggiungere solo quelli che mancano.

        reports_to_add = list_of_reports_id - existing_report_ids_with_permission

        if reports_to_add:
            self._repository.add_permissions(user_id=user_id, reports_id=reports_to_add, date=today)

        self._repository.add_existing_permission(user_id=user_id, reports_id=existing_report_ids_with_permission,
                                                 date=today)

    def get_permissions_in_pending(self, pf_id: str) -> List[PermissionPartialInfo]:

        permissions = self._repository.get_permissions_in_pending_by_pf_id(pf_id=pf_id)
        lst_of_permission_info = []

        for permission in permissions:
            permission_info = PermissionPartialInfo(
                user_id=permission.user_id,
                created=permission.created,
                permission=permission.permission,
                report_id=permission.document_id)
            lst_of_permission_info.append(permission_info)

        return lst_of_permission_info

    def set_permissions(self, pf_id: str, permissions: List[PermissionToModify]) -> None:

        permissions_to_value = dict()

        for permission in permissions:
            permissions_to_value[(permission.user_id, str(permission.report_id))] = permission.permission

        self._repository.set_permissions(pf_id=pf_id, permissions_to_value=permissions_to_value)
