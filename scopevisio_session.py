import json
import logging
import time
import urllib.parse

import requests
import werkzeug.http
from requests import RequestException

from scopevisio_api_iterator import ScopevisioApiIterator
from scopevisio_error import ScopevisioError


class ScopevisioSession(object):
    """
    Context manager for a request session that loads cookies from a file at start
    """

    BASE_URL = 'https://appload.scopevisio.com/rest'

    def __init__(self, config):
        self.config = config
        self.tokens = None

    def __enter__(self):
        self.tokens = self.__authenticate(self.config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def request(self, method, url, **kwargs):
        # In case a request fails max_attempts are made to fetch the result...
        max_attempts = 5
        for attempt in range(max_attempts):
            acceptable_status_codes = kwargs.pop('acceptable_status_codes', [200])
            headers = kwargs.pop('headers', {})
            if self.tokens:
                access_token = self.tokens['access_token']
                headers = headers | {'Authorization': f'Bearer {access_token}'}
            try:
                response = requests.request(method, url, headers=headers, **kwargs)
                if response.status_code not in acceptable_status_codes:
                    raise ScopevisioError(response=response)
                return response
            except RequestException as err:
                logging.warning(
                    f'{err.__class__.__name__} (status {err.response.status_code}) retry {attempt + 1}/{max_attempts}')
                if attempt + 1 < max_attempts:
                    time.sleep(1)
                else:
                    logging.error(err.response.text)
                    raise err  # rethrow

    def request_json(self, method, url, **kwargs):
        response = self.request(method, url, **kwargs)
        if response.headers['content-type'] != 'application/json':
            raise ScopevisioError('response does not contain JSON', response=response)
        return json.loads(response.text)

    def __authenticate(self, config):
        payload = {
            'grant_type': 'password',
            'customer': config['customer'],
            'organisation': config['organisation'],
            'username': config['username'],
            'password': config['password'],
            'requestcookie': False
        }
        data = urllib.parse.urlencode(payload)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        return self.request_json(method='POST', url=self.BASE_URL + '/token', headers=headers, data=data)

    def get_journal(self):
        url = self.BASE_URL + '/journal'
        order = ['rowNumber = asc']
        return ScopevisioApiIterator(self, url=url, limit=1000, order=order)

    def download_document(self, document_number, documents_folder_path):
        headers = {
            'Accept': '*/*'
        }
        url = self.BASE_URL + '/journal/' + document_number + '/file'
        response = self.request(method='GET', url=url, headers=headers, acceptable_status_codes=[200, 404])
        if response.status_code == 404:
            logging.info(f'{document_number}: does not exist')
            return
        filename = document_number
        filename_in_response = self.__get_filename_from_response(response)
        if filename_in_response:
            filename += ' ' + filename_in_response
        path = documents_folder_path.joinpath(filename)
        with path.open('wb') as file:
            file.write(response.content)
        logging.info(f'{document_number}: downloaded as "{filename}"')

    @staticmethod
    def __get_filename_from_response(response):
        cd = response.headers.get('content-disposition')
        if not cd:
            return None
        content_type, options = werkzeug.http.parse_options_header(cd)
        if 'filename' not in options:
            return None
        return options['filename']
