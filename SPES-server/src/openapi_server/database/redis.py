from typing import List

import redis
import uuid

GLOBAL_DEFAULT_EXPIRED_TIME = 900  # 15 minutes


class ReportSessionRedis:
    _NAME = "ReportSession"
    _DEFAULT_EXPIRED_TIME = GLOBAL_DEFAULT_EXPIRED_TIME

    def __init__(self, host: str, port: int, db: int, password: str):
        self.redis = redis.Redis(host=host, port=port, db=db, password=password)


    def add_to_session(self, **kwargs) -> object:
        """
        Aggiunge alla sessione un singolo report.

        :param kwargs: Attributi da aggiungere come un unica entry. Tra questi figura lo user_id e il report_id.
            expire_time indica un tempo di expire custom.
            Si possono aggiungere anche altri attributi.
        :return:
        """
        expire_time = self._DEFAULT_EXPIRED_TIME
        if "expire_time" in kwargs.keys():
            expire_time = kwargs["expire_time"]
            kwargs.pop("expire_time")
        user_id = kwargs['user_id']
        # check if the entry already exists
        for entry in self.redis.scan_iter(f"{self._NAME}:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in self.redis.hgetall(entry).items()}
            if str(data['user_id']) == user_id and str(data['report_id']) == kwargs['report_id']:
                return 'Entry already exist'
            print(data)
        kwargs['row_id'] = uuid.uuid4().hex
        key = f"{self._NAME}:{user_id}:{kwargs['report_id']}"
        # store report to redis
        [self.redis.hset(key, index, value) for index, value in kwargs.items()]
        # set expired report entry
        self.redis.expire(key, expire_time)
        self.redis.expire(key, expire_time)
        result = {key.decode('utf-8'): value.decode('utf-8') for key, value in self.redis.hgetall(key).items()}
        return result

    def reports(self, user_id: str) -> List[object]:
        """
        Restituisce tutti i report della sessione.

        :param user_id: L'id dello user della sessione.
        :return: Una lista di report.
        """
        result = []
        for user_carts in self.redis.scan_iter(f"{self._NAME}:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in
                    self.redis.hgetall(user_carts).items()}
            result.append(data)
        return result

    def delete_report_by_row_id(self, user_id: str, row_id: str) -> int:
        """
        Cancella il report dalla sessione sulla base del row_id.

        :param user_id: L'id dello user della sessione.
        :param row_id:
        :return:
        """
        return self.redis.delete(f"{self._NAME}:{user_id}:{row_id}")

    def delete_report_by_id(self, user_id: str, report_id: str) -> int:
        """
         Cancella il report dalla sessione sulla base del report_id.

        :param user_id: L'id dello user della sessione.
        :param report_id: L'id del report medico.
        :return:
        """
        return self.redis.delete(f"{self._NAME}:{user_id}:{report_id}")

    def delete_all_reports(self, user_id: str) -> object:
        """
        Cancella l'intera sessione.

        :param user_id: L'id dello user della sessione.
        :return:
        """

        [self.redis.delete(x) for x in self.redis.scan_iter(f"{self._NAME}:{user_id}:*")]
