"""Containers module."""
import redis as redis
from dependency_injector import containers, providers

from database.database import Database
from database.redis import ReportSessionRedis
from repositories.document_repository import DocumentRepository
from repositories.person_repository import PersonRepository
from services.document_service import DocumentService
from services.permission_service import PermissionService
from services.person_service import PersonService
from services.report_service import ReportService
from services.user_service import UserService
from repositories.user_repository import UserRepository
from repositories.report_repository import ReportRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["apis.pf_api", "apis.report_api", "apis.wallet_api", "apis.auth_api", "security_api"])

    config = providers.Configuration(yaml_files=["config.yml"])
    db = providers.Singleton(Database, db_url=config.db.url, drop_on_startup=config.db.drop_on_startup,
                             startup_sql_path=config.db.startup_sql_path)

    reportSessionRedis = providers.Singleton(ReportSessionRedis, host=config.redis.host, port=config.redis.port, db=config.redis.db, password=config.redis.password)

    """
    Definizioni classi singleton repositories.
    """

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    person_repository = providers.Factory(
        PersonRepository,
        session_factory=db.provided.session,
    )
    report_repository = providers.Factory(
        ReportRepository,
        session_factory=db.provided.session,
    )
    document_repository = providers.Factory(
        DocumentRepository,
        session_factory=db.provided.session,
    )

    """
    Definizioni classi singleton services.
    """

    person_service = providers.Factory(
        PersonService,
        person_repository=person_repository,
    )

    document_service = providers.Factory(
        DocumentService,
        document_repository=document_repository,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        person_repository=person_repository
    )

    report_service = providers.Factory(
        ReportService,
        report_repository=report_repository,
        session_repository=reportSessionRedis.provided
    )

    permission_service = providers.Factory(
        PermissionService,
        report_repository=report_repository,
    )
