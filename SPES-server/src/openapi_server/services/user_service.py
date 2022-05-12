"""Services module."""

from typing import Dict

from models.user_info import UserInfoWithPwd
from repositories.person_repository import PersonRepository
from repositories.repository_exceptions import UserNotFoundError
from repositories.user_repository import UserRepository
from utils.utils import verify_password, get_password_hash, create_username, generate_random_password
import auth_handler


class UserService:
    """
    Questa classe definisce i servizi relativi all'entità User per gestire l'autenticaziione
    """

    def __init__(self, user_repository: UserRepository, person_repository: PersonRepository) -> None:
        self._repository: UserRepository = user_repository
        self._person_repository: PersonRepository = person_repository

    def auth(self, username: str, password: str) -> (Dict[str, str], bool):

        """

        :param username:
        :param password:
        :return:
        """

        pf_id = ""
        user = self._repository.get_by_username(username)
        first_access = user.first_access

        if user.first_access:
            self._repository.update_user_first_access(user_id=user.id)

        if user.role == "PF":
            pf_id = self._person_repository.get_person_id_by_user_id(user.id)

        if verify_password(plain_password=password, hashed_password=user.pwd):
            encoded_token = auth_handler.signJWT(user_id=user.id, user_role=user.role, pf_id=pf_id)
            return encoded_token, first_access
        else:
            raise UserNotFoundError(entity_id=None)

    def check_auth(self, token):
        decoded_token = auth_handler.decodeJWT(token=token)
        if decoded_token is None:
            return False
        else:
            user = self._repository.get_by_username(decoded_token["user_id"])
            if user.role == decoded_token["user_role"]:
                return True

    def check_auth2(self, token: str):
        return auth_handler.decodeJWT(token=token)

    def get_expires_auth(self, token: str):
        return auth_handler.decodeJWT(token=token)["expires"]

    def update_user(self, pf_id: str, old_pwd: str, new_pwd: str) -> None:
        """

        :param pf_id:
        :param old_pwd:
        :param new_pwd:
        :return:
        """

        new_hashed_pwd = get_password_hash(new_pwd)

        user = self._repository.update_user_by_pf_id(pf_id=pf_id, old_pwd=old_pwd, new_hashed_pwd=new_hashed_pwd)

        return UserInfoWithPwd(username=user.username)
