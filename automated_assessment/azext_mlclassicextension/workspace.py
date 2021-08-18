from .workspace_locations import WORKSPACE_LOCATIONS
from .api_client import APIClient

class MLClassicWorkspace(object):

    def __init__(self, workspace_id, azure_location, api_endpoint, access_token, trace=False):
        self.__workspace_id = workspace_id
        self.__azure_location = azure_location
        self.__access_token = access_token
        self.__api_endpoint = api_endpoint
        self.__ml_classic_location = WORKSPACE_LOCATIONS[azure_location]
        self.__api = APIClient(self.__ml_classic_location, api_endpoint, access_token, trace=trace)

    def get_details(self):
        
        return self.__api.get_workspace_details(self.__workspace_id)

    def get_project_containers(self):

        return self.__api.get_project_containers(self.__workspace_id)

    def get_experiments(self):

        return self.__api.get_experiments(self.__workspace_id)

    def get_experiment_details(self, experiment_id):

        return self.__api.get_experiment_details(self.__workspace_id, experiment_id)

    def get_webservices(self):

        return self.__api.get_webservices(self.__workspace_id)
    
    def get_webservice_details(self, webservice_id):

        return self.__api.get_webservice_details(self.__workspace_id, webservice_id)

    def get_trained_models(self):

        return self.__api.get_trained_models(self.__workspace_id)

    def get_transform_modules(self):

        return self.__api.get_transform_modules(self.__workspace_id)

    def get_webservice_groups(self):

        return self.__api.get_webservice_groups(self.__workspace_id)

    def get_webservice_group(self, webservice_group_id):

        return self.__api.get_webservice_group(self.__workspace_id, webservice_group_id)

    def get_datasources(self):

        return self.__api.get_datasources(self.__workspace_id)