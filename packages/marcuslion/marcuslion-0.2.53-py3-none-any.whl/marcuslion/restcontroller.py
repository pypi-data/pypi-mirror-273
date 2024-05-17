import json
import os.path

import pandas as pd
import urllib3

from marcuslion.apiUtils import get_filename_from_api
import marcuslion.config as config


def _get_server_url(is_backend) -> str:
    if is_backend:
        return config.get_backend_base_url() + '/' + config.get_backend_api_version() + '/'
    return config.get_base_url() + '/' + config.get_api_version() + '/'


class RestController:
    """
    MarcusLion RestController class
    """
    _http = urllib3.PoolManager()

    def __init__(self, url_path):
        self._url_path = url_path
        pass

    def _get_url(self, action, is_backend=False) -> str:
        full_url = _get_server_url(is_backend) + self._url_path
        if action is not None and len(action) > 0:
            full_url += '/' + action

        full_url = full_url.replace('//', '/').replace(':/', '://')
        return full_url

    def _get_request(self, action, params=None, method="GET", preload_content=True, **kwargs):
        if params is None:
            params = {}
        is_backend = False
        if 'is_backend' in params:
            is_backend = params['is_backend']
            del params['is_backend']

        full_url = self._get_url(action, is_backend)

        print(f"_get_request {method} {full_url} {params}")

        if kwargs.get('headers') is None:
            kwargs['headers'] = {
                'X-MARCUSLION-API-KEY': config.get_api_key()
            }
        else:
            kwargs['headers']['X-MARCUSLION-API-KEY'] = config.get_api_key()

        resp = self._http.request(method, full_url,
                                  fields=params,
                                  preload_content=preload_content,
                                  **kwargs)

        if resp.status == 401:
            raise ValueError("401: Unauthorized User. URL:" + full_url)
        if resp.status != 200:
            raise ValueError("status: " + full_url + " -> " + (
                str(resp.status) + (" data: " + resp.data.decode()) if resp.data else ""))
        return resp

    def upload_file(self, action, file_path, params=None):
        if params is None:
            params = {}

        params['file'] = (os.path.basename(file_path), open(file_path, 'rb').read())
        return self.verify_get(action, params, method="POST")

    def download_file(self, action, params, output_path=None):
        if output_path is None:
            output_path = "."
        resp = self._get_request(action, params, preload_content=False)
        file_name = f"{output_path}/{get_filename_from_api(resp)}"
        # create file_path if it does not exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        with open(file_name, 'wb+') as out_file:
            for chunk in resp.stream(1024):
                out_file.write(chunk)

        return out_file.name

    def verify_get_df(self, action=None, params=None) -> pd.DataFrame:
        response = self.verify_get(action, params)
        return pd.DataFrame.from_records(response)

    def verify_get(self, action, params=None, method="GET", preload_content=True, **kwargs) -> any:
        # Sending a GET request and getting back response as HTTPResponse object.
        resp = self._get_request(action, params, method, preload_content, **kwargs)

        data_str = resp.data.decode()
        if len(data_str) == 0:
            return None
        try:
            return json.loads(data_str)
        except ValueError as e:
            return data_str

    def verify_get_data(self, action=None, params=None) -> pd.DataFrame:
        data = self.verify_get(action, params)
        if data is None:
            return pd.DataFrame()
        df = pd.DataFrame(data['data'])
        return df
