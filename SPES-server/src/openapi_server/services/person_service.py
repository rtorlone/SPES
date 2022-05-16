"""Services module."""

from datetime import date
from typing import List
from uuid import uuid4

from models.address import Address
from models.citizenship import Citizenship
from models.marital_status import MaritalStatus
from models.pf_info import PfInfo, PfInfoWithIds, PfUserInfo, PFPartialInfoWithIds, PfInfoWithIdsForUpdate, PfId
from repositories.person_repository import PersonRepository
from utils.utils import create_username, generate_random_password, get_password_hash, generate_list_of_ids


class PersonService:
    """
    Questa classe definisce i servizi relativi all'entità Person
    """

    def __init__(self, person_repository: PersonRepository) -> None:
        self._repository: PersonRepository = person_repository

    def create_person(self, creator_id: str, item: PfInfo) -> PfUserInfo:
        """
        Crea la persona fragile e salvala nel repository.

        :param creator_id: Lo user id dell'utente che vuole creare la persona fragile.
        :param item: Oggetto di tipo PfInfo contente tutte le info della persona fragile.
        :return: un oggetto PfId
        """
        id = str(uuid4())
        user_id = str(uuid4())
        username = create_username(item.firstname, item.lastname)
        plain_pwd = generate_random_password()
        hashed_pwd = get_password_hash(plain_pwd)
        today = date.today()

        person = self._repository.add_person(id=id,
                                             created_by=creator_id,
                                             owner_id=creator_id,
                                             is_dead=item.is_dead,
                                             death_date=item.death_date,
                                             email = item.email,
                                             cf=item.cf,
                                             cui_code=item.cui_code,
                                             firstname=item.firstname,
                                             lastname=item.lastname,
                                             fullname=item.fullname,
                                             nicknames=item.nicknames,
                                             gender=item.gender,
                                             birth_date=item.birth_date,
                                             verified=item.verified,
                                             created=today,
                                             updated=today,
                                             sanitary_district_id=item.sanitary_district_id,
                                             user_id=user_id,
                                             birth_nation_id=item.birth_nation_id,
                                             birth_geoarea_id=item.birth_geoarea_id,
                                             birth_city=item.birth_city,
                                             is_foreign=item.is_foreign,
                                             is_anonymous=item.is_anonymous,
                                             username=username,
                                             pwd=hashed_pwd)

        # Aggiungo gli indirizzi
        if item.address_list:
            lst_ids = generate_list_of_ids(n=len(item.address_list))
            self._repository.add_addresses(user_id=creator_id, pf_id=person.id, items=item.address_list, ids=lst_ids,
                                           today=today)

        # Aggiungo i marital status
        if item.marital_status_list:
            lst_ids = generate_list_of_ids(n=len(item.marital_status_list))
            self._repository.add_marital_statuses(user_id=creator_id, pf_id=person.id, items=item.marital_status_list,
                                                  ids=lst_ids, today=today)

        # Aggiungo le cittadinanze
        if item.citizenship_list:
            lst_ids = generate_list_of_ids(n=len(item.citizenship_list))
            self._repository.add_citizenship(user_id=creator_id, pf_id=person.id, items=item.citizenship_list,
                                             ids=lst_ids, today=today)

        return PfUserInfo(pf_id=person.id, email=item.email, username=username, password=plain_pwd)

    def get_person(self, pf_id: str) -> PfInfoWithIds:
        """
        Restituisce la persona in base al suo id.

        :param pf_id: L'id della persona fragile
        :return: Un oggetto di tipo PfInfo
        """
        person = self._repository.get_person_by_pf_id(pf_id)

        address_info_dict = {}
        for address in person.addresses:
            address_info = Address(from_date=address.from_date,
                                   address=address.address,
                                   geoarea_id=address.geoarea_id,
                                   address_type_id=address.address_type_id)
            address_info_dict[address.id] = address_info

        marital_status_info_dict = {}
        for marital_status in person.marital_status:
            marital_status_info = MaritalStatus(from_date=marital_status.from_date,
                                                marital_status_code=marital_status.marital_status_code)
            marital_status_info_dict[marital_status.id] = marital_status_info

        citizenship_info_dict = {}
        for citizenship in person.citizenships:
            citizenship_info = Citizenship(from_date=citizenship.from_date,
                                           nation_id=citizenship.nation_id)
            citizenship_info_dict[citizenship.id] = citizenship_info

        person_info = PfInfoWithIds(
            pf_id=person.id,
            firstname=person.firstname,
            lastname=person.lastname,
            fullname=person.fullname,
            cf=person.cf,
            gender=person.gender,
            nicknames=person.nicknames,
            birth_date=person.birth_date,
            birth_nation_id=person.birth_nation_id,
            birth_geoarea_id=person.birth_geoarea_id,
            birth_city=person.birth_city,
            cui_code=person.cui_code,
            sanitary_district_id=person.sanitary_district_id,
            is_foreign=person.is_foreign,
            is_anonymous=person.is_anonymous,
            verified=person.verified,
            is_dead=person.is_dead,
            death_date=person.death_date,
            address_list=address_info_dict,
            citizenship_list=citizenship_info_dict,
            marital_status_list=marital_status_info_dict
        )
        return person_info

    def get_person_id(self, user_id: str) -> str:
        """
        Ottiene l'id della persona fragile a partire dal suo user_id.

        :param user_id: Lo user id della persona fragile.
        :return: L'id della persona fragile.
        """
        person_id = self._repository.get_person_id_by_user_id(user_id=user_id)
        return person_id

    def update_person(self, user_id: str, pf_id: str, item: PfInfoWithIdsForUpdate) -> PfId:
        """
        Aggiorna le informazioni della persona fragile.

        :param user_id:
        :param item:
        :param pf_id: id della persona fragile
        :return: Un oggetto di tipo PfId
        """
        today = date.today()

        person = self._repository.update_person(pf_id=pf_id,
                                                is_dead=item.is_dead,
                                                death_date=item.death_date,
                                                cf=item.cf,
                                                cui_code=item.cui_code,
                                                firstname=item.firstname,
                                                lastname=item.lastname,
                                                fullname=item.fullname,
                                                nicknames=item.nicknames,
                                                gender=item.gender,
                                                birth_date=item.birth_date,
                                                verified=item.verified,
                                                updated=today,
                                                sanitary_district_id=item.sanitary_district_id,
                                                birth_nation_id=item.birth_nation_id,
                                                birth_geoarea_id=item.birth_geoarea_id,
                                                birth_city=item.birth_city,
                                                is_foreign=item.is_foreign,
                                                is_anonymous=item.is_anonymous)
        # Modifica
        if item.address_list_to_update:
            self._repository.update_addresses(user_id=user_id, pf_id=pf_id, items=item.address_list_to_update,
                                              today=today)
        if item.citizenship_list_to_update:
            self._repository.update_citizenship(user_id=user_id, pf_id=pf_id, items=item.citizenship_list_to_update,
                                                today=today)
        if item.marital_status_list_to_update:
            self._repository.update_marital_statuses(user_id=user_id, pf_id=pf_id,
                                                     items=item.marital_status_list_to_update, today=today)

        # Aggiungi
        if item.address_list_to_add:
            lst_ids = generate_list_of_ids(n=len(item.address_list_to_add))
            self._repository.add_addresses(user_id=user_id, pf_id=pf_id, items=item.address_list_to_add, ids=lst_ids,
                                           today=today)
        if item.citizenship_list_to_add:
            lst_ids = generate_list_of_ids(n=len(item.citizenship_list_to_add))
            self._repository.add_citizenship(user_id=user_id, pf_id=pf_id, items=item.citizenship_list_to_add,
                                           ids=lst_ids, today=today)
        if item.marital_status_list_to_add:
            lst_ids = generate_list_of_ids(n=len(item.marital_status_list_to_add))
            self._repository.add_marital_statuses(user_id=user_id, pf_id=pf_id, items=item.marital_status_list_to_add,
                                           ids=lst_ids, today=today)

        # Cancella
        if item.address_list_to_delete:
            self._repository.remove_addresses(user_id=user_id, pf_id=pf_id, ids=item.address_list_to_delete)
        if item.marital_status_list_to_delete:
            self._repository.remove_martital_statuses(user_id=user_id, pf_id=pf_id,
                                                      ids=item.marital_status_list_to_delete)
        if item.citizenship_list_to_delete:
            self._repository.remove_citizenship(user_id=user_id, pf_id=pf_id, ids=item.citizenship_list_to_delete)

        return PfId(id=person.id)

    def add_address_by_pf_id(self, user_id: str, pf_id: str, items: List[Address]) -> PfId:
        """

        :param user_id:
        :param pf_id:
        :param items:
        :return:
        """

        today = date.today()

        lst_ids = generate_list_of_ids(n=len(items))
        self._repository.add_addresses(user_id=user_id, pf_id=pf_id, items=items, ids=lst_ids,
                                       today=today)

        return lst_ids

    def add_citizenship_by_pf_id(self, user_id: str, pf_id: str, items: List[Citizenship]) -> PfId:
        """

        :param user_id:
        :param pf_id:
        :param items:
        :return:
        """

        today = date.today()

        lst_ids = generate_list_of_ids(n=len(items))
        self._repository.add_citizenship(user_id=user_id, pf_id=pf_id, items=items, ids=lst_ids,
                                         today=today)

        return lst_ids

    def add_marital_status_by_pf_id(self, user_id: str, pf_id: str, items: List[MaritalStatus]) -> PfId:
        """

        :param user_id:
        :param pf_id:
        :param items:
        :return:
        """

        today = date.today()

        lst_ids = generate_list_of_ids(n=len(items))
        self._repository.add_marital_statuses(user_id=user_id, pf_id=pf_id, items=items, ids=lst_ids,
                                              today=today)

        return lst_ids

    def get_persons_by_query(self, firstname: str, lastname: str, nicknames: str, cf: str, limit: str, offset: str,
                             is_anonymous: bool = None, is_foreign: bool = None, is_dead: bool = None,
                             verified: bool = None) -> List[PFPartialInfoWithIds]:

        """
        Effettua una query in base a dei parametri di ricerca.

        :param verified: Parametro di ricerca.
        :param is_dead: Parametro di ricerca.
        :param is_foreign: Parametro di ricerca.
        :param is_anonymous: Parametro di ricerca.
        :param firstname: Parametro di ricerca.
        :param lastname: Parametro di ricerca.
        :param nicknames: Parametro di ricerca.
        :param cf: Parametro di ricerca.
        :param offset: Offset della query.
        :param limit: Limite degli oggetti da recuperare.
        :return: Una lista di oggetti di tipo Person
        """

        if limit >= 1000:
            limit = 1000

        persons = self._repository.get_persons_by_query(firstname=firstname, lastname=lastname, nicknames=nicknames,
                                                        cf=cf,
                                                        is_anonymous=is_anonymous, is_foreign=is_foreign,
                                                        is_dead=is_dead, verified=verified, offset=offset, limit=limit)
        persons_info_list = []

        for person in persons:
            person_info = PFPartialInfoWithIds(
                pf_id=person.id,
                firstname=person.firstname,
                lastname=person.lastname,
                cf=person.cf,
                gender=person.gender,
                nicknames=person.nicknames,
                birth_date=person.birth_date,
                cui_code=person.cui_code,
                is_foreign=person.is_foreign,
                is_anonymous=person.is_anonymous,
                verified=person.verified,
                is_dead=person.is_dead
            )
            persons_info_list.append(person_info)

        return persons_info_list


