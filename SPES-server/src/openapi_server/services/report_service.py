"""Services module."""
import os
import uuid

from datetime import date

from typing import List

from fastapi import UploadFile

from database.redis_deprecated import ReportSessionRedis

from repositories.report_repository import ReportRepository
from repositories.repository_exceptions import ReportNotFoundError, UploadReportError, FormatReportError, \
    PersonNotFoundError, UserNotFoundError
from models.report_info import ReportInfo, ReportOnlyId
from sqlalchemy.exc import IntegrityError
from fastapi.responses import FileResponse


class ReportService:
    """
    Questa classe definisce i servizi relativi all'entità Report.
    """

    BASE_PATH = "../../reports/"
    SUPPORTED_MEDIA_TYPE = ["application/pdf"]

    def __init__(self, report_repository: ReportRepository, session_repository: ReportSessionRedis) -> None:
        self._repository: ReportRepository = report_repository
        self._session_repository: ReportSessionRedis = session_repository

    def get_reports(self, user_id: str) -> List[ReportInfo]:
        """
        Restituisce tutti i referti medici di cui l'utente ha i permessi.

        :param user_id: L'id dell'utente
        :return: un lista di oggetti di tipo ReportInfo
        """
        permissions = self._repository.get_permissions_with_filter(user_id=user_id, pending=False, permission=True)
        list_of_report_info = []
        for permission in permissions:
            report = permission.document
            report_info = ReportInfo(report_id=report.id,
                                     title=report.title,
                                     upload_date=report.upload_date,
                                     permission=permission.permission)
            list_of_report_info.append(report_info)

        return list_of_report_info

    def get_reports_by_pf_id(self, pf_id: str) -> List[ReportInfo]:
        """
        Restituisce una lista di report solo se questi ultimi sono posseduti dalla persona fragile.

        :param pf_id: L'id della persona fragile.
        :return: Una lista dii oggetti dii tipo ReportInfo
        """

        reports = self._repository.get_reports(pf_id=pf_id)
        list_of_report_info = []
        for report in reports:
            report_info = ReportInfo(report_id=report.id,
                                     title=report.title,
                                     upload_date=report.upload_date,
                                     permission=None)
            list_of_report_info.append(report_info)

        return list_of_report_info

    def get_reports_by_user_id_and_pf_id(self, user_id: str, pf_id: str) -> List[ReportInfo]:
        """
        Restituisce tutti i referti medici relativi ad una persona fragile di cui l'utente ha i permessi.
        In caso mancassero i permessi relativi ad un report, verrà comunque restituito con permission value pari a None.

        :param user_id: l'id dello user che richiede i referti.
        :param pf_id: l'id della persona fragile.
        :return: una lista di oggetti ReportInfo
        """

        reports = self._repository.get_reports(pf_id=pf_id)

        list_of_report = []
        for report in reports:
            permissions = report.permissions
            permission_value = None
            pending_value = None
            for permission in permissions:
                if permission.user_id == user_id:
                    permission_value = permission.permission
                    pending_value = permission.pending
                    break
                else:
                    permission_value = None
            report_info = ReportInfo(report_id=report.id,
                                     title=report.title,
                                     upload_date=report.upload_date,
                                     permission=permission_value,
                                     pending=pending_value)
            list_of_report.append(report_info)

        return list_of_report

    def get_report(self, user_id: str, report_id: str) -> FileResponse:
        """
        Restituisce il report in base all'id, solamente se lo user in questione possiede i permessi.

        :param user_id: L'id dello user che deve avere i permessi.
        :param report_id: L'id del report.
        :return: Un oggetto di tipo FileResponse, che contiene negli header i metadati relativi al report.
        """

        report = self._repository.get_report(user_id=user_id, report_id=report_id)
        headers = {"report_id": report.id, "title": report.title, "upload_date": str(report.upload_date)}
        report_response = FileResponse(report.path, headers=headers, media_type="application/pdf")
        return report_response

    def get_report_by_owner(self, pf_id: str, report_id: str) -> FileResponse:
        """
        Restituisce il report in base al report_id e pf_id

        :param pf_id:
        :param report_id:
        :return: Un oggetto di tipo FileResponse, che contiene negli header i metadati relativi al report.
        """
        report = self._repository.get_report_pf_id_and_report_id(pf_id=pf_id, report_id=report_id)
        headers = {"report_id": report.id, "title": report.title, "upload_date": str(report.upload_date)}
        report_response = FileResponse(report.path, headers=headers, media_type="application/pdf")
        return report_response

    def upload_report(self, user_id: str, pf_id: str, title: str, file: UploadFile) -> ReportOnlyId:
        """
        Salva il report sul filesystem del server e i relativi metadati nel repository.

        :param user_id: L'id dello user che vuole inserire il report.
        :param pf_id: l'id della persona fragile.
        :param title: Il titolo del referto medico.
        :param file: Il file da salvare nel filesystem.
        :return: Un oggetto ReportOnlyId
        """
        report_id = str(uuid.uuid4())
        file_path = self.BASE_PATH + report_id + ".pdf"
        contents = file.file.read()
        if title is None: title = report_id

        if file.content_type not in self.SUPPORTED_MEDIA_TYPE:
            raise FormatReportError(entity_id=report_id, media_type=file.content_type)

        # Salva su filesystem
        with open(file_path, 'wb') as f:
            f.write(contents)
            f.close()

        today = date.today()

        # Salva i metadati sul repository
        try:
            report = self._repository.insert_report(user_id=user_id, pf_id=pf_id, report_id=report_id, title=title,
                                                    upload_date=today, path=file_path)
            print(report)
            return ReportOnlyId(report_id=report_id)
        except IntegrityError as err:
            os.remove(file_path)
            if "pf_id" in str(err.orig):
                raise PersonNotFoundError(entity_id=pf_id)
            if "upload_by" in str(err.orig):
                raise UserNotFoundError(entity_id=pf_id)
        except Exception:
            os.remove(file_path)
            raise UploadReportError(entity_id=report_id)

    def add_reports_to_session(self, user_id: str, report_ids: List[ReportOnlyId]) -> int:
        """
        Aggiunge alla sessione dell'utente i report specificati nella lista degli id.

        :param user_id: L'id dello user della sessione.
        :param report_ids: Lista di report id.
        :return: None.
        """

        list_of_report_ids = []
        for report in report_ids:
            list_of_report_ids.append(str(report.report_id))

        reports = self._repository.get_reports_by_report_ids(report_ids=list_of_report_ids)

        for report in reports:
            self._session_repository.add_to_session(user_id=user_id, report_id=report.id, title=report.title,
                                                    upload_date=str(report.upload_date))
        return len(self._session_repository.reports(user_id=user_id))

    def get_reports_from_session(self, user_id: str) -> List[ReportInfo]:

        """
        Restituisce una lista di report appartenti alla sessione dell'utente.

        :param user_id: L'id dello user della sessione.
        :return: Una lista di oggetti ReportInfo
        """

        reports_from_session = self._session_repository.reports(user_id=user_id)
        if not reports_from_session:
            raise ReportNotFoundError(entity_id=None)

        list_of_report_info = []

        for report in reports_from_session:
            report_info = ReportInfo(report_id=report["report_id"], title=report["title"],
                                     upload_date=report["upload_date"])
            list_of_report_info.append(report_info)

        return list_of_report_info

    def delete_reports_from_session(self, user_id: str) -> None:
        """
        Cancella tutti i report dalla sessione.

        :param user_id: L'id dello user della sessione.
        :return: None
        """
        self._session_repository.delete_all_reports(user_id=user_id)

    def delete_reports_from_session_by_report_id(self, user_id: str, report_id: str) -> None:
        """
        Cancella il report specificato dalla sessione.

        :param user_id: L'id dello user della sessione.
        :return: None.
        """
        return_value = self._session_repository.delete_report_by_id(user_id=user_id, report_id=report_id)
        if return_value == 0:
            raise ReportNotFoundError(entity_id=report_id)
