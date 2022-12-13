from queue import Empty
from datetime import datetime
import logging
from utils import Sample, Increment

class MatchMaker:
    def __init__(self, internal_users: object, external_users: object, run_date: str = '2017-02-02') -> None:
        self._internal_users = internal_users
        self._external_users = external_users
        self._run_date = run_date
        self._internal_matches = list()
        self._external_matches = list()
        self._merged = list()
        self._i = Increment()
        self._s = Sample()
        self._logger = logging.getLogger("main")

    @property
    def internal_users(self) -> object:
        return self._internal_users
    
    @internal_users.setter
    def internal_users(self, value: object) -> None:
        self._internal_users = value

    @property
    def external_users(self) -> object:
        return self._external_users
    
    @external_users.setter
    def external_users(self, value: object) -> None:
        self._external_users = value

    @property
    def run_date(self) -> str:
        return self._run_date

    @run_date.setter
    def run_date(self, value: str) -> None:
        self._run_date = value

    def main(self) -> list:
        self.external_users.start()
        external_queue = self.external_users.users_queue
        external_user = external_queue.get(timeout=1)
        external_unique = external_user['unique_key']
        self._logger.debug(f"First external user: {external_unique}")

        self.internal_users.start()
        internal_queue = self.internal_users.users_queue
        internal_user = internal_queue.get(timeout=20)
        internal_unique = internal_user['unique_key']
        self._logger.debug(f"First internal user: {internal_unique}")

        '''
        Below is a very rudimentary algorithm used to move
        users through the queue. Two FIFO queues handle
        next person up duties, if there's a match we grab
        both internal and external users and pop both off
        the list. 

        Next if the external users are ahead (since they have
        fewer records currently in their API) we pop users off
        until we match or surpass the external users.

        After that, we switch it up and do the same thing with
        the external users. We pop users off until we find a
        match or we pass the internal users.
        '''

        while True:
            try:
                if external_unique == internal_unique:
                    self._internal_matches.append(internal_user)
                    self._external_matches.append(external_user)
                    internal_user = internal_queue.get(timeout=20)
                    internal_unique = internal_user['unique_key']
                    external_user = external_queue.get(timeout=1)
                    external_unique = external_user['unique_key']
                elif external_unique > internal_unique:
                    internal_user = internal_queue.get(timeout=20)
                    internal_unique = internal_user['unique_key']
                elif external_unique < internal_unique:
                    external_user = external_queue.get(timeout=1)
                    external_unique = external_user['unique_key']
                else:
                    break
            except Empty:
                self._logger.debug("Done queueing.")
                self.external_users.terminate()
                self.internal_users.terminate()
                break

        return self.merge_records()

    def merge_records(self) -> list:
        '''
        We know that the two datasets were sorted by lastname so
        this is a very simple matching excercise based solely on index
        matches. We know we queued the users into the lists at the
        same time so we just have to retreive and build our insert
        records.

        We return the full list of merged users, this is something
        that I would have liked to address if I had more time. 
        This scales fine currently but won't be very memory friendly
        with a substantial number of records. 
        '''
        for i, user in enumerate(self._internal_matches):
            vendor_last_active_date_str = self._external_matches[i]['last_active_date']
            vendor_last_active_date = self.get_date_from_string("%Y-%m-%d", vendor_last_active_date_str)
            d = {
                "doximity_id": int(user['id']),
                "vendor_id": self._external_matches[i]['id'],
                "run_date": self.run_date,
                "doximity_last_active_date": user['last_active_date'],
                "vendor_last_active_date": vendor_last_active_date_str,
                "is_doximity_active": True if user['is_active'] == 1 else False,
                "is_vendor_active": self.is_active(vendor_last_active_date),
                "emitted_at": datetime.now(tz=None).strftime("%Y-%m-%d %H:%M:%S.%f")
            }
            self._merged.append(d)
            self._i.add()
        return self._merged

    def get_date_from_string(self, pattern: str, date: str) -> datetime:
        return datetime.strptime(date, pattern).date()

    def is_active(self, date: str) -> bool:
        return (self.get_date_from_string("%Y-%m-%d", self.run_date) - date).days <= 30

    def get_total_matches_output(self) -> None:
        return str(self._i)

    def get_samples_output(self) -> None:
        for i in range(0, 10):
            self._s.add(self._merged[i])
        return str(self._s)