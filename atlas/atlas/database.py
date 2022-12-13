from threading import Thread
import json
import logging
from mysql.connector import Error
import mysql.connector

class Database(Thread):
    '''
    Generic database class that serves as a foundation for adding
    additional flavors as needed.
    '''
    def __init__(self, host, database, username, password) -> None:
        self._host = host
        self._database = database
        self._username = username
        self._password = password
        super(Database, self).__init__()

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str) -> None:
        self._host = value

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value: str) -> None:
        self._database = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        self._password = value

class MySQL(Database):
    '''
    Base MySQL class with just the functions needed to add and retreive
    data from the database.
    '''
    def __init__(self, host, database, username, password, port: str = '3306'):
        super().__init__(host, database, username, password)
        self._port = port
        self._logger = logging.getLogger("main")

    @property
    def port(self) -> str:
        return self._port

    @port.setter
    def port(self, value: str) -> None:
        self._port = value

    def new_connection(self):
        try:
            connection = mysql.connector.connect(host=self.host,
                                                 port=self.port,
                                                 database=self.database,
                                                 user=self.username,
                                                 password=self.password,
                                                 ssl_disabled=True)
            return connection
        except Error as e:
            self._logger.error(f"Error while connecting to MySQL. {e}")
            pass

    def sql_to_list(self, sql) -> list:
        connection = self.new_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            headers = [i[0] for i in cursor.description]
            results = cursor.fetchall()
            data = list()
            for result in results:
                data.append(dict(zip(headers, result)))
            return data
        finally:
            cursor.close()
            connection.close()

    def return_one(self, sql: str) -> str:
        connection = self.new_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            return result
        finally:
            cursor.close()
            connection.close()

    def commit_sql(self, sql:str) -> None:
        connection = self.new_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def list_of_dict_to_sql(self, table: str, l: list) -> None:
        '''
        Specific function that was built to take the list of dictionaries
        from the matched records and load them into the database as
        efficiently as possible.
        '''
        placeholder = ', '.join([f"%({i})s " for i in l[0].keys()])
        sql = f"""INSERT INTO `{table}` ({",".join(l[0].keys())}) 
        VALUES ({placeholder})"""
        connection = self.new_connection()
        try:
            cursor = connection.cursor()
            cursor.executemany(sql, l)
            connection.commit()
        finally:
            cursor.close()
            connection.close()