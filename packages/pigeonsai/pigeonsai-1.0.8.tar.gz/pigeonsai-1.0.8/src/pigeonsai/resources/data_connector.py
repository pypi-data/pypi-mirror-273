# resources/data_connector.py
from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from typing import Literal
from .._constants import (BASE_URL_V2)

import httpx
import os
import json
import pandas as pd

if TYPE_CHECKING:
    from .._client import PigeonsAI


class DataConnector:
    data_connection_uri_global = None
    train_set_uri_global = None

    def __init__(self, client: PigeonsAI):
        self.client = client

    def create_connector(
        self,
        connection_name: str,
        connection_type: Literal['postgres', 'mysql', 'mongodb'],
        db_host: Optional[str] = None,
        db_name: Optional[str] = None,
        db_username: Optional[str] = None,
        db_password: Optional[str] = None,
        db_port: Optional[int] = None,
        mongodb_uri: Optional[str] = None
    ):
        if connection_type not in ['postgres', 'mysql', 'mongodb']:
            raise ValueError("Invalid connection type. Please choose 'postgres', 'mysql', or 'mongodb'.")
        
        if connection_type in ['postgres', 'mysql']:
            if not all([db_host, db_name, db_username, db_password, db_port]):
                missing = [name for name, value in locals().items() if not value and name.startswith('db_')]
                raise ValueError(f"Missing required parameters for {connection_type} connection: {', '.join(missing)}")
        elif connection_type == 'mongodb':
            if not mongodb_uri or not db_name:
                missing = []
                if not mongodb_uri:
                    missing.append('mongodb_uri')
                if not db_name:
                    missing.append('db_name')
                raise ValueError("Missing required parameters for MongoDB connection: " + ', '.join(missing))
        
        url = f"{BASE_URL_V2}/create-data-connector"
        headers = self.client.auth_headers
        data = {
            "data_connection_custom_name": connection_name,
            "data_connection_type": connection_type,
            "data_connection_host": db_host,
            "data_connection_port": db_port,
            "data_connection_database_name": db_name,
            "data_connection_username": db_username,
            "data_connection_password": db_password,
            "data_connection_mongodb_uri": mongodb_uri
        }

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        _data = response_json['data']

        DataConnector.data_connection_uri_global = _data['data_connection_uri']

        filtered_res = {
            'id': _data['id'],
            'created_at': _data['created_at'],
            'created_by': _data['created_by'],
            'data_connection_uri': _data['data_connection_uri'],
        }

        print(
            f'\033[38;2;85;87;93m Connector creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
        print(f'\033[38;2;85;87;93m Data connector URI:\033[0m \033[92m{_data["data_connection_uri"]}\033[0m')

        return filtered_res

    def create_train_set(
        self,
        type: str,
        train_set_name: str,
        columns_map: dict,
        file_path: str = None,
        data_connection_uri: str = None,
        table_name: str = None,
    ):

        # Use the global data_connection_uri if not provided
        if not data_connection_uri and DataConnector.data_connection_uri_global:
            data_connection_uri = DataConnector.data_connection_uri_global

        type = type.lower()
        if not type:
            print('Please provide type as either file or connection. Use file option if you want to upload file or use connection if you want to fetch data directly from the database using data connector. ')
            return

        headers = self.client.auth_headers

        if type == 'file':
            if not file_path:
                print('Missing file path.')
                return
            return _prepare_data_with_file(
                headers=headers,
                train_set_name=train_set_name,
                file_path=file_path,
                columns_map=columns_map
            )

        if type == 'connection':
            if not table_name:
                print('Missing table name. table_name param is the name of the table you want to fetch data from.')
                return

            if not data_connection_uri:
                print('Missing data_connection_uri. data_connection_uri param is the uri of the data connection.')
                return

            if not table_name:
                print('Missing table name. table_name param is the name of the table you want to fetch data from.')
                return

            return _prepare_data_with_connector(
                client=self.client,
                headers=headers,
                train_set_name=train_set_name,
                data_connection_uri=data_connection_uri,
                table_name=table_name,
                columns_map=columns_map
            )

    def revision_train_set_with_file(
        self,
        train_set_uri: str,
        file_path: str,
    ):
        url = f"{BASE_URL_V2}/revision-train-dataset-with-file"
        headers = self.client.auth_headers
        if 'Content-Type' in headers:
            headers.pop('Content-Type')
        data = {
            'train_set_uri': train_set_uri,
        }

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f)}
                response = httpx.post(url, headers=headers, files=files, data=data, timeout=300.0)
                response.raise_for_status()
            response_json = response.json()

            train_dataset_uri = response_json['data']

            filtered_res = {
                'train_set_uri': train_dataset_uri
            }

            DataConnector.train_set_uri_global = train_dataset_uri

            print(
                f'\033[38;2;85;87;93m Train set new revision creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
            print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{train_dataset_uri}\033[0m')

            return filtered_res
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, detail: {e.response.text}"
            print(error_message)
        except Exception as e:
            print(f'Status code: {e.response.status_code}, detail: {e.response.text}')
            raise e

    def revision_train_set_with_connector(
        self,
        train_set_uri: str,
    ):
        url = f"{BASE_URL_V2}/revision-train-dataset-with-connector"
        headers = self.client.auth_headers

        data = {'train_set_uri': train_set_uri}

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        train_dataset_uri = response_json['data']

        filtered_res = {
            'train_set_uri': train_dataset_uri
        }

        DataConnector.train_set_uri_global = train_dataset_uri

        print(
            f'\033[38;2;85;87;93m Train set creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
        print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{train_dataset_uri}\033[0m')

        return filtered_res

    def delete_train_set(self, train_set_uri: str):
        url = f"{BASE_URL_V2}/delete-train-dataset"
        data = {"train_set_uri": train_set_uri}
        headers = self.client.auth_headers

        return self.client._request("POST", url, headers=headers, data=data)

    def delete_data_connector(self, data_connector_uri: str):
        url = f"{BASE_URL_V2}/delete-data-connector"
        data = {"data_connector_uri": data_connector_uri}
        headers = self.client.auth_headers

        return self.client._request("POST", url, headers=headers, data=data)


def _prepare_data_with_file(
    headers,
    train_set_name: str,
    file_path: str,
    columns_map: dict
):
    url = f"{BASE_URL_V2}/create-train-dataset-with-file"
    
    df = pd.read_csv(file_path, nrows=0)
    csv_headers = df.columns.tolist()

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    if 'Content-Type' in headers:
        headers.pop('Content-Type')

    data = {
        'train_dataset_name': train_set_name,
        'file_name': file_name,
        'file_size': str(file_size),
        'csv_header': json.dumps(csv_headers),
        'columns_map': json.dumps(columns_map)
    }
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = httpx.post(url, headers=headers, files=files, data=data, timeout=300.0)
            response.raise_for_status()
        response_json = response.json()

        _data = response_json['data']

        filtered_res = {
            'id': _data['id'],
            'created_at': _data.get('created_at'),
            'created_by': _data.get('created_by'),
            'train_set_uri': _data.get('train_dataset_uri')
        }

        DataConnector.train_set_uri_global = _data.get("train_dataset_uri", "")

        print(
            f'\033[38;2;85;87;93m Train set creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
        print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{_data.get("train_dataset_uri", "")}\033[0m')

        return filtered_res
    except Exception as e:
        print(f'Status code: {e.response.status_code}, detail: {e.response.text}')
        raise e


def _prepare_data_with_connector(
    client: PigeonsAI,
    train_set_name: str,
    data_connection_uri: str,
    table_name: str,
    columns_map: dict,
    headers,
):
    url = f"{BASE_URL_V2}/create-train-dataset-with-connector"
    data = {
        'train_dataset_name': train_set_name,
        'data_connection_uri': data_connection_uri,
        'table_name': table_name,
        'columns_map': columns_map
    }
    response = client._request("POST", url, headers=headers, data=data)
    response_json = response.json()

    _data = response_json['data']

    filtered_res = {
        'id': _data['id'],
        'created_at': _data.get('created_at'),
        'created_by': _data.get('created_by'),
        'train_set_uri': _data.get('train_dataset_uri')
    }

    DataConnector.train_set_uri_global = _data.get("train_dataset_uri", "")

    print(
        f'\033[38;2;85;87;93m Train set creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
    print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{_data.get("train_dataset_uri", "")}\033[0m')

    return filtered_res
