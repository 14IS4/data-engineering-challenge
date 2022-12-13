from threading import Thread
from queue import Queue, Empty
import math
import requests
import queue
import logging
from utils import Increment

class VendorApi(Thread):
    '''
    Generic base class that can be extended for specific endpoints or specific API versions.
    '''
    def __init__(self, base_url: str, api_version: int, endpoint: str) -> None:
        super(VendorApi, self).__init__()
        self._base_url = base_url
        self._api_version = api_version
        self._endpoint = endpoint
        self.total_pages = self.get_total_pages()
        self._logger = logging.getLogger("main")

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._base_url = value

    @property
    def api_version(self) -> str:
        return self._api_version

    @api_version.setter
    def api_version(self, value: int) -> None:
        self._api_version = value

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value: str) -> None:
        self._endpoint = value

    def get_full_url(self, page: int, endpoint: str) -> str:
        return f"{self.base_url}/v{self.api_version}/{endpoint}?page={page}"

    def get_data(self, page: int, obj: str) -> list:
        '''
        Generic getter that will pull an endpoint based on the endpoint name and page number.
        '''
        try:
            url = self.get_full_url(page=page, endpoint=self.endpoint)
            resp = requests.get(url)
            if resp.status_code == 200:
                json_response = resp.json()
                return json_response.get(obj)
        except Exception as e:
            self._logger.error(f"Could not retrieve data: {e}")

    def get_total_pages(self) -> int:
        return int(self.get_data(page=0, obj='total_pages'))

    def get_page_size(self, page: int, obj: str) -> int:
        return len(self.get_data(page=page, obj=obj))

class UsersV1(VendorApi):
    '''
    User specific extention of the Vendor API class, provides an example of options for adding 
    new endpoints in the future or handling breaking changes with new versions of the API.
    '''
    def __init__(self, base_url: str = 'https://de-tech-challenge-api.herokuapp.com/api', obj: str = 'users', percentage: int = 10) -> None:
        super().__init__(base_url, api_version=1, endpoint='users')
        self._obj = obj
        self._percentage = percentage
        self.page_size = self.get_page_size(page=1, obj=self.obj)
        self.total_users = self.get_total_users()
        self.slice = self.get_subset_user_count()
        self._run_queue = None
        self._users_queue = None
        self._logger = logging.getLogger("main")

    @property
    def obj(self) -> str:
        return self._obj

    @obj.setter
    def obj(self, value: str) -> None:
        self._obj = value

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

    def get_users(self, page: int) -> list:
        return self.get_data(page=page, obj=self.obj)

    def get_total_users(self) -> int:
        last_page = self.get_page_size(page=self.total_pages, obj=self.obj)
        return (((self.total_pages - 1) * self.page_size) + last_page)

    def get_subset_user_count(self) -> int:
        return int((self.percentage / 100.00) * self.total_users)

    def get_page_from_slice(self, slice: int) -> int:
        return math.ceil(slice / self.page_size)

    def build_run_queue(self) -> None:
        self.run_queue = Queue(maxsize=2)
    
    def build_users_queue(self) -> None:
        self.users_queue = Queue(maxsize=self.slice)

    def terminate(self) -> None:
        self.run_queue.get(timeout=1)
        while True:
            try:
                self.users_queue.get(timeout=0.1)
            except Empty:
                self._logger.debug(f"Queue terminated")
                break

    def run(self) -> None:
        '''
        Main function that fills the queue and is put in it's own worker thread.
        '''
        page = Increment(1)
        self.build_run_queue()
        self.run_queue.put("running")
        self.build_users_queue()
        while True:
            self._logger.debug(f"Processing page: {page.value}")
            if self.run_queue.empty():
                return
            users = self.get_users(page=page.value)
            for user in users:
                ### unique_key is built using the same lastname, firstname, location to join back to the
                ### internal data.
                user['unique_key'] = f"{user['lastname']}{user['firstname']}{user['practice_location']}".lower()
                self.users_queue.put(user)
            page.add()
            if page.value > self.total_pages:
                break