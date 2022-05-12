from typing import List

import redis
import uuid

redis = redis.Redis(host='localhost', port=6379, db=1, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")

GLOBAL_DEFAULT_EXPIRED_TIME = 900  # 15 minutes


class ReportSessionRedis:
    _NAME = "ReportSession"
    _DEFAULT_EXPIRED_TIME = GLOBAL_DEFAULT_EXPIRED_TIME

    @classmethod
    def add_to_session(cls, **kwargs) -> object:
        """
        Aggiunge alla sessione un singolo report.

        :param kwargs: Attributi da aggiungere come un unica entry. Tra questi figura lo user_id e il report_id.
            expire_time indica un tempo di expire custom.
            Si possono aggiungere anche altri attributi.
        :return:
        """
        expire_time = cls._DEFAULT_EXPIRED_TIME
        if "expire_time" in kwargs.keys():
            expire_time = kwargs["expire_time"]
            kwargs.pop("expire_time")
        user_id = kwargs['user_id']
        # check if the entry already exists
        for entry in redis.scan_iter(f"{cls._NAME}:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in redis.hgetall(entry).items()}
            if str(data['user_id']) == user_id and str(data['report_id']) == kwargs['report_id']:
                return 'Entry already exist'
            print(data)
        kwargs['row_id'] = uuid.uuid4().hex
        key = f"{cls._NAME}:{user_id}:{kwargs['report_id']}"
        # store report to redis
        [redis.hset(key, index, value) for index, value in kwargs.items()]
        # set expired report entry
        redis.expire(key, expire_time)
        redis.expire(key, expire_time)
        result = {key.decode('utf-8'): value.decode('utf-8') for key, value in redis.hgetall(key).items()}
        return result

    @classmethod
    def reports(cls, user_id: str) -> List[object]:
        """
        Restituisce tutti i report della sessione.

        :param user_id: L'id dello user della sessione.
        :return: Una lista di report.
        """
        result = []
        for user_carts in redis.scan_iter(f"{cls._NAME}:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in redis.hgetall(user_carts).items()}
            result.append(data)
        return result

    @classmethod
    def delete_report_by_row_id(cls, user_id: str, row_id: str) -> int:
        """
        Cancella il report dalla sessione sulla base del row_id.

        :param user_id: L'id dello user della sessione.
        :param row_id:
        :return:
        """
        return redis.delete(f"{cls._NAME}:{user_id}:{row_id}")

    @classmethod
    def delete_report_by_id(cls, user_id: str, report_id: str) -> int:
        """
         Cancella il report dalla sessione sulla base del report_id.

        :param user_id: L'id dello user della sessione.
        :param report_id: L'id del report medico.
        :return:
        """
        return redis.delete(f"{cls._NAME}:{user_id}:{report_id}")

    @classmethod
    def delete_all_reports(cls, user_id: str) -> object:
        """
        Cancella l'intera sessione.

        :param user_id: L'id dello user della sessione.
        :return:
        """

        [redis.delete(x) for x in redis.scan_iter(f"{cls._NAME}:{user_id}:*")]
