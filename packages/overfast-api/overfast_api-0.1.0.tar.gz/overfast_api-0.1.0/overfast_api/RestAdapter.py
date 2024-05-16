import requests
import requests.packages
from typing import Dict, List
from overfast_api.models import Result
from overfast_api.exceptions import OverfastException
from json import JSONDecodeError


class RestAdapter:
    def __init__(self, hostname: str = "overfast-api.tekrop.fr", ssl_verify: bool = True):
        """
        Construction for RestAdapter class

        :param hostname: Normally  overfast-api.tekrop.fr
        :param ssl_verify: Normally True, but set to false if having SSL/TLS validation issues
        """
        self.url = f"https://{hostname}/"
        self.ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, params: Dict = None) -> Result:
        """
        Base function for HTTP requests to the REST API

        :param http_method: HTTP method to use
        :param endpoint: API endpoint to use
        :param params: HTTP request parameters to pass in requests
        :return: Returns an OverFastAPI Result object
        """
        full_url = f"{self.url}{endpoint}"
        try:
            response = requests.request(method=http_method, url=full_url, params=params, verify=self.ssl_verify)
        except requests.exceptions.RequestException as e:
            raise OverfastException("RequestException", e)

        try:
            data_out = response.json()
        except (JSONDecodeError, ValueError) as e:
            raise OverfastException("Bad JSON in response", e)

        if response.status_code == 422:
            raise OverfastException(
                f"Bad Request {data_out['detail'][0]['type']} - {data_out['detail'][0]['loc']}"
            )
        else:
            return Result(status_code=response.status_code, data=data_out if type(data_out) is list else [data_out])

    def get(self, endpoint: str, params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, params=params)

    def post(self, endpoint: str, params: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, params=params)

    def delete(self, endpoint: str, params: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, params=params)