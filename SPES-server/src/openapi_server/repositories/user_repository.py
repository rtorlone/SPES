"""Repositories module."""

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Dict

from sqlalchemy.orm import Session

from database.person import Person
from database.user import User

from repositories.repository_exceptions import UserNotFoundError, PersonNotFoundError
from utils.utils import verify_password


class UserRepository:
    """
    Questa classe rappresenta il repository per l'entità User
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_by_username(self, username: str) -> User:
        """
        Recupera l'utente sulla base dell'id.

        :param username:
        :return: Un oggetto di tipo User
        """

        with self.session_factory() as session:
            user = session.query(User).filter(User.username == username).first()

            if not user:
                raise UserNotFoundError(entity_id=username)

            return user

    def update_user_first_access(self, user_id: str) -> User:
        """
        Aggiorna lo stato di primo accesso dello user specifciato.

        :param user_id: L'id dello user.
        :return: Un oggetto di tipo User
        """

        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                raise UserNotFoundError(entity_id=user_id)

            user.first_access = False
            session.commit()
            return user

    def update_user_by_pf_id(self, pf_id, old_pwd: str, new_hashed_pwd: str):
        """

        :param pf_id:
        :param old_pwd:
        :param new_hashed_pwd:
        :return:
        """

        with self.session_factory() as session:
            user = session.query(Person).filter(Person.id == pf_id).from_self(User).join(Person.user).first()
            if not user:
                raise PersonNotFoundError(entity_id=pf_id)
            if not verify_password(hashed_password=user.pwd, plain_password=old_pwd):
                raise PersonNotFoundError(entity_id=pf_id)

            if new_hashed_pwd:
                user.pwd = new_hashed_pwd

            session.commit()
            session.refresh(user)

            return user
