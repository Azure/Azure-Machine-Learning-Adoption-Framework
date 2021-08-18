from knack.help_files import helps
from azure.cli.core import AzCommandsLoader
from .workspace import MLClassicWorkspace

# TODO: extend help switch to support all mlclassic extension commands

helps['mlclassic workspace show'] = """
    type: command
    short-summary: Displays the properties of an Azure ML Classic workspace.
"""

helps['mlclassic workspace projects'] = """
    type: command
    short-summary: Gets the list of projects in an Azure ML Classic workspace.
"""

helps['mlclassic workspace experiments'] = """
    type: command
    short-summary: Gets the list of experiments an Azure ML Classic workspace.
"""

helps['mlclassic workspace experiment'] = """
    type: command
    short-summary: Displays the properties of an Azure ML Classic experiment.
"""

helps['mlclassic workspace webservices'] = """
    type: command
    short-summary: Gets the list of webservices in an Azure ML Classic workspace.
"""

helps['mlclassic workspace webservice'] = """
    type: command
    short-summary: Displays the properties of an Azure ML Classic webservice.
"""

helps['mlclassic workspace trainedmodels'] = """
    type: command
    short-summary: Gets the list of trained models in an Azure ML Classic workspace.
"""

helps['mlclassic workspace transformmodules'] = """
    type: command
    short-summary: Gets the list of transform modules in an Azure ML Classic workspace.
"""

helps['mlclassic workspace webservicegroups'] = """
    type: command
    short-summary: Gets the list of webservice groups in an Azure ML Classic workspace.
"""

helps['mlclassic workspace webservicegroup'] = """
    type: command
    short-summary: Displays the properties of an Azure ML Classic webservice group.
"""

helps['mlclassic workspace datasources'] = """
    type: command
    short-summary: Gets the list of data sources in an Azure ML Classic workspace.
"""

def show_workspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):
    
    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_details()

def get_project_containers(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):
    
    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_project_containers()

def get_experiments(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_experiments()

def get_experiment_details(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token, experiment_id):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_experiment_details(experiment_id)

def get_webservices(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_webservices()

def get_webservice_details(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token, webservice_id):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_webservice_details(webservice_id)

def get_trained_models(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_trained_models()

def get_transform_modules(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_transform_modules()

def get_webservice_groups(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_webservice_groups()

def get_webservice_group(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token, webservice_group_id):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_webservice_group(webservice_group_id)

def get_datasources(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token):

    ws = MLClassicWorkspace(workspace_id, workspace_location, workspace_api_endpoint,  workspace_access_token)
    return ws.get_datasources()

class MLClassicCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        custom_type = CliCommandType(operations_tmpl='azext_mlclassicextension#{}')
        super(MLClassicCommandsLoader, self).__init__(cli_ctx=cli_ctx,
                                                       custom_command_type=custom_type)

    def load_command_table(self, args):
        with self.command_group('mlclassic workspace') as g:
            g.custom_command('show', 'show_workspace')
            g.custom_command('projects', 'get_project_containers')
            g.custom_command('experiments', 'get_experiments')
            g.custom_command('experiment', 'get_experiment_details')
            g.custom_command('webservices', 'get_webservices')
            g.custom_command('webservice', 'get_webservice_details')
            g.custom_command('trainedmodels', 'get_trained_models')
            g.custom_command('transformmodules', 'get_transform_modules')
            g.custom_command('webservicegroups', 'get_webservice_groups')
            g.custom_command('webservicegroup', 'get_webservice_group')
            g.custom_command('datasources', 'get_datasources')
        return self.command_table

    def load_arguments(self, _):
        with self.argument_context('mlclassic workspace') as c:
            c.argument('workspace_id', options_list=['-wid', '--workspace-id'], type=str, help='The id of the Azure ML Classic workspace.')
            c.argument('workspace_location', options_list=['-wl', '--workspace-location'], type=str, help='The location of the Azure ML Classic workspace.')
            c.argument('workspace_api_endpoint', options_list=['-wapi', '--workspace-api-endpoint'], type=str, help='The API endpoint servicing the Azure ML Classic workspace.')
            c.argument('workspace_access_token', options_list=['-wat', '--workspace-access-token'], type=str, help='The access token for the Azure ML Classic workspace.')
        with self.argument_context('mlclassic workspace experiment') as c:
            c.argument('experiment_id', options_list=['-eid', '--experiment-id'], type=str, help='The id of the Azure ML Classic experiment.')
        with self.argument_context('mlclassic workspace webservice') as c:
            c.argument('webservice_id', options_list=['-wsid', '--webservice-id'], type=str, help='The id of the Azure ML Classic webservice.')
        with self.argument_context('mlclassic workspace webservicegroup') as c:
            c.argument('webservice_group_id', options_list=['-wsgid', '--webservice-group-id'], type=str, help='The id of the Azure ML Classic webservice group.')
        pass

COMMAND_LOADER_CLS = MLClassicCommandsLoader