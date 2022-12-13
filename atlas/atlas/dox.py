from queue import Queue, Empty
import logging
from database import MySQL
from utils import Increment, DDL

class DoxMySQLRead(MySQL):
    '''
    Extends the MySQL class that was built as a generic base class.
    '''
    def __init__(
            self, 
            host,
            database,
            username,
            password,
            port: str = '3306',
            run_date: str = '2017-02-02',
            percentage: int = 10
        ) -> None:
        super().__init__(host, database, username, password, port)
        self._run_date = run_date
        self._percentage = percentage
        self._offset = 0
        self.total_users = self.get_total_users()
        self.slice = self.get_subset_user_count()
        self._run_queue = None
        self._users_queue = None
        self._logger = logging.getLogger("main")

    @property
    def run_date(self) -> str:
        return self._run_date

    @run_date.setter
    def run_date(self, value: str) -> None:
        self._run_date = value

    @property
    def offset(self) -> str:
        return self._offset

    @offset.setter
    def offset(self, value: str) -> None:
        self._offset = value

    @property
    def percentage(self) -> str:
        return self._percentage

    @percentage.setter
    def percentage(self, value: str) -> None:
        self._percentage = value

    @property
    def run_queue(self) -> str:
        return self._run_queue

    @run_queue.setter
    def run_queue(self, value: str) -> None:
        self._run_queue = value

    @property
    def users_queue(self) -> str:
        return self._users_queue

    @users_queue.setter
    def users_queue(self, value: str) -> None:
        self._users_queue = value

    def get_users(self) -> list:
        '''
        Gets the full list of users from the Doximity MySQL instance. Determines active date
        and builds a unique key based off of firstname, lastname and location to join to.
        '''
        sql = f"""
        SELECT  user.id,
                user.last_active_date,
                CASE 
                    WHEN user.last_active_date >= DATE_SUB("{self.run_date}", INTERVAL 30 DAY)
                    THEN True
                    ELSE False
                END AS is_active,
                LOWER(CONCAT(user.lastname,user.firstname,user_practice.location)) AS unique_key
        FROM    user
        JOIN    user_practice
        ON      user.practice_id = user_practice.id
        ORDER BY user.Lastname
        LIMIT   {self.offset}, {self.slice};
        """
        self._logger.debug(f"Users Query: {sql}")
        data = self.sql_to_list(sql)
        return data

    def get_total_users(self) -> int:
        '''
        Sets a baseline for how big our slice needs to be based on the passed in percentage.
        '''
        sql = "SELECT COUNT(id) FROM user"
        result = self.return_one(sql)
        return int(result)

    def get_distinct_users(self) -> int:
        '''
            *** Reference function, not used *** 
        Determines if the unique_key is truely unique. Without location
        the firstname and lastname alone had duplicate records. Pulls 
        the distinct count of unique keys
        '''
        sql = f"""
        SELECT  COUNT(DISTINCT unique_key)
        FROM    (
                    SELECT  CONCAT(user.lastname,user.firstname,user_practice.location) AS unique_key
                    FROM    user
                    JOIN    user_practice
                    ON      user.practice_id = user_practice.id
        ) AS user
        """
        result = self.return_one(sql)
        return int(result)

    def is_key_unique(self) -> bool:
        '''
            *** Reference function, not used *** 
        Determines if the unique_key is truely unique. Without location
        the firstname and lastname alone had duplicate records.
        '''
        return self.total_users == self.get_distinct_users()

    def get_subset_user_count(self) -> int:
        '''
        Determines slice that we can use to batch the data into queues with.
        '''
        return int((self.percentage / 100.00) * self.total_users)

    def build_run_queue(self) -> None:
        self.run_queue = Queue(maxsize=2)
    
    def build_users_queue(self) -> None:
        self.users_queue = Queue(maxsize=self.slice)

    def terminate(self) -> None:
        self.run_queue.get(timeout=1)
        while True:
            try:
                self.users_queue.get(timeout=0.01)
            except Empty:
                break

    def run(self) -> None:
        '''
        Main function that fills the queue and is put in it's own worker thread.
        '''
        i = Increment()
        self.build_run_queue()
        self.run_queue.put("running")
        self.build_users_queue()
        while True:
            self._logger.debug(f"Processing rows: {self.offset + 1} to {self.slice + self.offset + 1}")
            if self.run_queue.empty():
                break
            users = self.get_users()
            for user in users:
                self.users_queue.put(user)
                i.add()
            self.offset += (self.slice + 1)
            if i.value == self.total_users:
                break

class DoxMySQLWrite(MySQL):
    '''
    Extends the MySQL class that was built as a generic base class.
    '''
    def __init__(
            self, 
            host,
            database,
            username,
            password,
            port: str = '3306',
            run_date: str = '2017-02-02'
        ) -> None:
        super().__init__(host, database, username, password, port)
        self._run_date = run_date

    @property
    def run_date(self) -> str:
        return self._run_date

    @run_date.setter
    def run_date(self, value: str) -> None:
        self._run_date = value

    def build_user_match_table(self) -> None:
        sql = DDL
        self.commit_sql(sql)

    def rerun(self) -> None:
        sql = f"DELETE FROM user_match WHERE run_date = '{self.run_date}';"
        self.commit_sql(sql)