"""Repositories module."""

from contextlib import AbstractContextManager
from datetime import date
from typing import Callable, Iterator, Dict, List

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from database.person import Person
from database.person_address import PersonAddress
from database.person_citizenship import PersonCitizenship
from database.person_marital_status import PersonMaritalStatus
from database.user import User
from models.address import Address, AddressWithId
from models.citizenship import Citizenship
from models.pf_info import PfInfo

from repositories.repository_exceptions import PersonNotFoundError, AddressNotFoundError, CitizenshipNotFoundError, \
    MaritalStatusNotFoundError, UserNotFoundError


class PersonRepository:
    """
    Questa classe rappresenta il repository per l'entita Person.
    """

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Person]:
        with self.session_factory() as session:
            return session.query(Person).all()

    def get_person_by_pf_id(self, pf_id: str) -> Person:
        """
        Interroga il repository per restituire una specifica persona fragile.

        :param pf_id: L'id della persona fragile.
        :return: un oggetto di tipo Person.
        """
        with self.session_factory() as session:
            person = session.query(Person).filter(Person.id == pf_id).options(joinedload(Person.addresses),
                                                                              joinedload(Person.marital_status),
                                                                              joinedload(Person.citizenships)).first()
            if not person:
                raise PersonNotFoundError(pf_id)
            return person

    def get_person_id_by_user_id(self, user_id: str):
        with self.session_factory() as session:
            person = session.query(Person).filter(Person.user_id == user_id).first()
            if not person:
                raise PersonNotFoundError(user_id)
            return person.id

    def add_person(self, id: str, created_by: str, owner_id: str, is_dead: bool, death_date: date, cf: str,
                   cui_code: str,
                   firstname: str, lastname: str, fullname: str, email:str, nicknames: str, gender: str, birth_date: date,
                   verified: bool,
                   created: date, updated: date, sanitary_district_id: str, is_anonymous: bool, is_foreign: bool,
                   birth_city: str,
                   birth_geoarea_id: str, birth_nation_id: str, user_id: str, username: str, pwd: str) -> Person:
        """
        Aggiunge una persona fragile nel repository.

        :param id:
        :param created_by:
        :param owner_id:
        :param is_dead:
        :param death_date:
        :param cf:
        :param cui_code:
        :param firstname:
        :param lastname:
        :param fullname:
        :param nicknames:
        :param gender:
        :param birth_date:
        :param verified:
        :param created:
        :param updated:
        :param sanitary_district_id:
        :param is_anonymous:
        :param is_foreign:
        :param birth_city:
        :param birth_geoarea_id:
        :param birth_nation_id:
        :param user_id:
        :return: Un oggetto di tipo Person.
        """
        with self.session_factory() as session:
            user = User(id=user_id, username=username, pwd=pwd, email=email, role="PF")
            person = Person(id=id,
                            created_by=created_by,
                            owner_id=owner_id,
                            is_dead=is_dead,
                            death_date=death_date,
                            cf=cf,
                            cui_code=cui_code,
                            firstname=firstname,
                            lastname=lastname,
                            fullname=fullname,
                            nicknames=nicknames,
                            gender=gender,
                            birth_date=birth_date,
                            verified=verified,
                            created=created,
                            updated=updated,
                            sanitary_district_id=sanitary_district_id,
                            user_id=user_id,
                            birth_nation_id=birth_nation_id,
                            birth_geoarea_id=birth_geoarea_id,
                            birth_city=birth_city,
                            is_foreign=is_foreign,
                            is_anonymous=is_anonymous)

            session.add(user)
            session.add(person)
            session.commit()
            session.refresh(person)
            return person

    def add_addresses(self, user_id: str, pf_id: str, items: List[Address], ids: List[str],
                      today: date) -> PersonAddress:
        """
        Aggiunge gli indirizzi della persona fragile nel repository.

        :param user_id:
        :param pf_id:
        :param items:
        :param ids:
        :param today:
        :return: Un oggetto di tipo PersonAddress
        """

        with self.session_factory() as session:
            for address_info, id in zip(items, ids):
                address = PersonAddress(id=id,
                                        created_by=user_id,
                                        owner_id=user_id,
                                        pf_id=pf_id,
                                        address_type_id=address_info.address_type_id,
                                        geoarea_id=address_info.geoarea_id,
                                        address=address_info.address,
                                        from_date=address_info.from_date,
                                        created=today,
                                        updated=today)

                session.add(address)
            try:
                session.commit()
            except IntegrityError as err:
                if "pf_id" in str(err.orig):
                    raise PersonNotFoundError(entity_id=pf_id)
                if "created_by" in str(err.orig):
                    raise UserNotFoundError(entity_id=pf_id)

    def add_marital_statuses(self, user_id: str, pf_id: str, items: List[Address], ids: List[str],
                             today: date) -> PersonMaritalStatus:
        """
        Aggiunge i marital_status della persona fragile nel repository.

        :param user_id:
        :param pf_id:
        :param items:
        :param ids:
        :param today:
        :return: Un oggetto di tipo PersonMaritalStatus
        """

        with self.session_factory() as session:
            for marital_info, id in zip(items, ids):
                marital_status = PersonMaritalStatus(id=id,
                                                     created_by=user_id,
                                                     owner_id=user_id,
                                                     pf_id=pf_id,
                                                     marital_status_code=marital_info.marital_status_code,
                                                     from_date=marital_info.from_date,
                                                     created=today,
                                                     updated=today)

                session.add(marital_status)
            try:
                session.commit()
            except IntegrityError as err:
                if "pf_id" in str(err.orig):
                    raise PersonNotFoundError(entity_id=pf_id)
                if "created_by" in str(err.orig):
                    raise UserNotFoundError(entity_id=pf_id)

    def add_citizenship(self, user_id: str, pf_id: str, items: List[Address], ids: List[str],
                        today: date) -> PersonCitizenship:
        """
        Aggiunge le cittadinanze della persona fragile nel repository.

        :param user_id:
        :param pf_id:
        :param items:
        :param ids:
        :param today:
        :return: Un oggetto di tipo PersonCitizenship.
        """

        with self.session_factory() as session:
            for citizenship_info, id in zip(items, ids):
                citizenship = PersonCitizenship(id=id,
                                                created_by=user_id,
                                                owner_id=user_id,
                                                pf_id=pf_id,
                                                nation_id=citizenship_info.nation_id,
                                                from_date=citizenship_info.from_date,
                                                created=today,
                                                updated=today
                                                )

                session.add(citizenship)
            try:
                session.commit()
            except IntegrityError as err:
                if "pf_id" in str(err.orig):
                    raise PersonNotFoundError(entity_id=pf_id)
                if "created_by" in str(err.orig):
                    raise UserNotFoundError(entity_id=pf_id)

    def remove_addresses(self, user_id: str, pf_id: str, ids: List[str]) -> None:
        """
        Rimuove gli indirizzi specificati della persona fragile in questione.
        
        :param user_id: 
        :param pf_id: 
        :param ids: 
        :return: 
        """
        with self.session_factory() as session:
            person_addresses = session.query(PersonAddress).filter(
                (PersonAddress.pf_id == pf_id) & (PersonAddress.id.in_(ids))).all()

            if not person_addresses:
                raise AddressNotFoundError(entity_id=None)

            for person_address in person_addresses:
                session.delete(person_address)

            session.commit()
            return person_addresses

    def remove_citizenship(self, user_id: str, pf_id: str, ids: List[str]) -> None:
        """
        Rimuove le cittadinanze specificate della persona fragile in questione.

        :param user_id: 
        :param pf_id: 
        :param ids: 
        :return: 
        """
        with self.session_factory() as session:
            person_citizenships = session.query(PersonCitizenship).filter(
                (PersonCitizenship.pf_id == pf_id) & (PersonCitizenship.id.in_(ids))).all()

            if not person_citizenships:
                raise AddressNotFoundError(entity_id=None)

            for person_citizenship in person_citizenships:
                session.delete(person_citizenship)

            session.commit()
            return person_citizenships
    
    def remove_martital_statuses(self, user_id: str, pf_id: str, ids: List[str]) -> None:
        """
        Rimuove i martial_statuses specificati della persona fragile in questione.

        :param user_id: 
        :param pf_id: 
        :param ids: 
        :return: 
        """
        with self.session_factory() as session:
            person_marital_statuses = session.query(PersonMaritalStatus).filter(
                (PersonMaritalStatus.pf_id == pf_id) & (PersonMaritalStatus.id.in_(ids))).all()

            if not person_marital_statuses:
                raise AddressNotFoundError(entity_id=None)

            for person_marital_status in person_marital_statuses:
                session.delete(person_marital_status)

            session.commit()
            return person_marital_statuses

    def update_person(self, pf_id: str, is_dead: bool, death_date: date, cf: str,
                      cui_code: str,
                      firstname: str, lastname: str, fullname: str, nicknames: str, gender: str, birth_date: date,
                      verified: bool,
                      updated: date, sanitary_district_id: str, is_anonymous: bool, is_foreign: bool,
                      birth_city: str,
                      birth_geoarea_id: str, birth_nation_id: str) -> Person:
        """
        Aggiorna le informazioni di una persona fragile.

        :param pf_id:
        :param is_dead:
        :param death_date:
        :param cf:
        :param cui_code:
        :param firstname:
        :param lastname:
        :param fullname:
        :param nicknames:
        :param gender:
        :param birth_date:
        :param verified:
        :param updated:
        :param sanitary_district_id:
        :param is_anonymous:
        :param is_foreign:
        :param birth_city:
        :param birth_geoarea_id:
        :param birth_nation_id:
        :return:
        """

        with self.session_factory() as session:
            person: Person = session.query(Person).filter(Person.id == pf_id).first()
            if not person:
                raise PersonNotFoundError(pf_id)

            person.is_dead = is_dead
            person.death_date = death_date
            person.cf = cf
            person.cui_code = cui_code
            person.firstname = firstname
            person.lastname = lastname
            person.fullname = fullname
            person.nicknames = nicknames
            person.gender = gender
            person.birth_date = birth_date
            person.verified = verified
            person.updated = updated
            person.sanitary_district_id = sanitary_district_id
            person.birth_nation_id = birth_nation_id
            person.birth_geoarea_id = birth_geoarea_id
            person.birth_city = birth_city
            person.is_foreign = is_foreign
            person.is_anonymous = is_anonymous

            session.commit()
            session.refresh(person)
            return person

    def update_addresses(self, user_id: str, pf_id: str, items: Dict[str, Address], today: date) -> Iterator[
        PersonAddress]:
        """
        Aggiorna gli indirizzi della persona fragile nel repository.

        :param pf_id: L'id della persona fragile.
        :param user_id: Lo user id dello user che richiede l'aggiornamento.
        :param items: Gli oggetti da modificare.
        :param today: La data dell'aggiornamento.
        :return: Una lista di oggetti PersonAddress
        """

        with self.session_factory() as session:
            person_addresses = session.query(PersonAddress).filter(
                (PersonAddress.pf_id == pf_id) & (PersonAddress.id.in_(items.keys()))).all()

            if not person_addresses:
                raise AddressNotFoundError(entity_id=None)

            for person_address in person_addresses:
                person_address.address_type_id = items[person_address.id].address_type_id
                person_address.geoarea_id = items[person_address.id].geoarea_id
                person_address.address = items[person_address.id].address
                person_address.from_date = items[person_address.id].from_date
                person_address.updated = today

            session.commit()
            return person_addresses

    def update_citizenship(self, user_id: str, pf_id: str, items: Dict[str, Citizenship], today: date) -> Iterator[
        PersonCitizenship]:
        """
        Aggiorna le cittadinanze della persona fragile nel repository.

        :param pf_id: L'id della persona fragile.
        :param user_id: Lo user id dello user che richiede l'aggiornamento.
        :param items: Gli oggetti da modificare.
        :param today: La data dell'aggiornamento.
        :return: Una lista di oggetti PersonCitizenship
        """

        with self.session_factory() as session:
            person_citizenship = session.query(PersonCitizenship).filter(
                (PersonCitizenship.pf_id == pf_id) & (PersonCitizenship.id.in_(items.keys()))).all()

            if not person_citizenship:
                raise CitizenshipNotFoundError(entity_id=None)

            for person_citizenship in person_citizenship:
                person_citizenship.nation_id = items[person_citizenship.id].nation_id
                person_citizenship.from_date = items[person_citizenship.id].from_date
                person_citizenship.updated = today

            session.commit()
            return person_citizenship

    def update_marital_statuses(self, user_id: str, pf_id: str, items: Dict[str, Address], today: date) -> Iterator[
        PersonMaritalStatus]:
        """
        Aggiorna i marital status della persona fragile nel repository.

        :param pf_id: L'id della persona fragile.
        :param user_id: Lo user id dello user che richiede l'aggiornamento.
        :param items: Gli oggetti da modificare.
        :param today: La data dell'aggiornamento.
        :return: Una lista di oggetti PersonMaritalStatus
        """

        with self.session_factory() as session:
            marital_statuses = session.query(PersonMaritalStatus).filter(
                (PersonMaritalStatus.pf_id == pf_id) & (PersonMaritalStatus.id.in_(items.keys()))).all()

            if not marital_statuses:
                raise MaritalStatusNotFoundError(entity_id=None)

            for marital_status in marital_statuses:
                marital_status.marital_status_code = items[marital_status.id].marital_status_code
                marital_status.from_date = items[marital_status.id].from_date
                marital_status.updated = today

            session.commit()
            return marital_statuses

    def delete_person_by_id(self, user_id: str) -> None:
        """
        TODO
        :param user_id:
        :return:
        """
        with self.session_factory() as session:
            entity: Person = session.query(Person).filter(Person.id == user_id).first()
            if not entity:
                raise PersonNotFoundError(user_id)
            session.delete(entity)
            session.commit()

    def get_persons_by_query(self, firstname: str, lastname: str, nicknames: str, cf: str, offset: int, limit: int,
                             is_anonymous: bool = None, is_foreign: bool = None, is_dead: bool = None,
                             verified: bool = None) -> Iterator[Person]:
        """
        Restituisce una lista di Person sulla base di una query su vari parametri. I parametri di ricerca sono in and tra loro e sono case insensitive.

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

        with self.session_factory() as session:

            query = session.query(Person)

            if (firstname is not None) and not (firstname == ""):
                firstname_format = "%" + firstname + "%"
                query = query.filter(Person.firstname.ilike(firstname_format))
            if (lastname is not None) and not (lastname == ""):
                lastname_format = "%" + lastname + "%"
                query = query.filter(Person.lastname.ilike(lastname_format))
            if (nicknames is not None) and not (nicknames == ""):
                nicknames_format = "%" + nicknames + "%"
                query = query.filter(Person.nicknames.ilike(nicknames_format))
            if (cf is not None) and not (cf == ""):
                cf_format = "%" + cf + "%"
                query = query.filter(Person.cf.ilike(cf_format))
            if is_anonymous is not None:
                query = query.filter(Person.is_anonymous.is_(is_anonymous))
            if is_foreign is not None:
                query = query.filter(Person.is_foreign.is_(is_foreign))
            if is_dead is not None:
                query = query.filter(Person.is_dead.is_(is_dead))
            if verified is not None:
                query = query.filter(Person.verified.is_(verified))

            persons = query.order_by(desc(Person.firstname), desc(Person.lastname), desc(Person.nicknames),
                                     desc(Person.cf)).limit(
                limit).offset(offset).all()

            if not persons:
                raise PersonNotFoundError(entity_id=None)
            return persons