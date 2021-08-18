from urllib.parse import urljoin
import json
import requests

from .errors import AzureMLClassicHttpError

class APIClient(object):

    ACCESS_TOKEN_HEADER_NAME = 'x-ms-metaanalytics-authorizationtoken'
    ACCESS_TOKEN_MANAGEMENT_HEADER_NAME = 'authorization'
    CONTENT_TYPE_HEADER_NAME = 'Content-Type'
    CONTENT_TYPE_HEADER_VALUE_JSON = 'application/json;charset=UTF8'
    USER_AGENT_HEADER_NAME = 'User-Agent'
    USER_AGENT_HEADER_VALUE = 'mlclassic-azurecli-extension'
    API_BASE_URL = 'studioapi.azureml.net'
    API_MANAGEMENT_BASE_URL = 'management.azureml.net'

    def __init__(self, location, api_endpoint, access_token, trace=False):
        self.__location = location
        self.__access_token = access_token
        self.__api_url = api_endpoint
        # Handle the special case of South Central US which has a special management url.
        self.__api_management_url = f'https://{self.API_MANAGEMENT_BASE_URL}' if location == "ussouthcentral" else f'https://{location}.{self.API_MANAGEMENT_BASE_URL}'
        self.__trace = trace

    def get_workspace_details(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}')

    def get_project_containers(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/projectcontainers')

    def get_trained_models(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/trainedmodels')

    def get_transform_modules(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/transformmodules')

    def get_webservice_groups(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/webservicegroups')

    def get_webservice_group(self, workspace_id, webservice_group_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/webservicegroups/{webservice_group_id}')

    def get_datasources(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/datasources')

    def get_experiments(self, workspace_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/experiments')

    def get_experiment_details(self, workspace_id, experiment_id):

        return self.__send_get_req(f'api/workspaces/{workspace_id}/experiments/{experiment_id}')

    def get_webservices(self, workspace_id):

        return self.__send_management_get_req(f'workspaces/{workspace_id}/webservices')
    
    def get_webservice_details(self, workspace_id, webservice_id):

        return self.__send_management_get_req(f'workspaces/{workspace_id}/webservices/{webservice_id}')

    def __get_headers(self, content_type=None, management_endpoint=False):
        headers = {
            self.USER_AGENT_HEADER_NAME: self.USER_AGENT_HEADER_VALUE,
            self.CONTENT_TYPE_HEADER_NAME: self.CONTENT_TYPE_HEADER_VALUE_JSON
        }
        if content_type:
            headers[self.CONTENT_TYPE_HEADER_NAME] = content_type

        if management_endpoint:
            headers[self.ACCESS_TOKEN_MANAGEMENT_HEADER_NAME] = f'Bearer {self.__access_token}'
        else:
            headers[self.ACCESS_TOKEN_HEADER_NAME] = self.__access_token
        return headers

    def __parse_response(self, response):

        if response.status_code >= 400:
            raise AzureMLClassicHttpError(response.text, response.status_code)

        if response.status_code == 204: # no content
            return None

        return response.json()

    def __send_get_req(self, api_path):
        url = urljoin(self.__api_url, api_path)
        if self.__trace:
            print(f'Calling {url}...')
        response = requests.get(
            url=url,
            headers=self.__get_headers()
        )

        return self.__parse_response(response)

    def __send_post_req(self, api_path, data, content_type=None):
        url = urljoin(self.__api_url, api_path)
        if self.__trace:
            print(f'Calling {url}...')
        response = requests.post(
            url=url,
            data=data,
            headers=self.__get_headers(content_type)
        )

        return self.__parse_response(response)

    def __send_management_get_req(self, api_path):
        url = urljoin(self.__api_management_url, api_path)
        if self.__trace:
            print(f'Calling {url}...')
        response = requests.get(
            url=url,
            headers=self.__get_headers(management_endpoint=True)
        )

        return self.__parse_response(response)