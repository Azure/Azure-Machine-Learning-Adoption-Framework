# Azure Machine Learning Adoption Framework Automated Assessment Tool

This tool is an Azure CLI exention to automatically list Machine Learning Studio(classic) assets (worksapce, web services, datasets, experiments etc) of a given subscription. It helps to inventory ML Studio(classic) assets and locate assets owner. 

## Build the automated assessment tool

To build the automated assessment tool, run the following command in the `automated_assessment` folder (make sure you have an active Pyhon environment):

```ps
python setup.py bdist_wheel
```

## Use the automated assessment tool

>**NOTE**
>
>The examples below demonstrate the use of Azure CLI (including the ML Classic extension) in a PowerShell environment. For more details on AZ execution environments, check the [Choose the right command-line tool for Azure](https://docs.microsoft.com/en-us/cli/azure/choose-the-right-azure-command-line-tool) section in the documentation.

1. Install the `az mlclassic` extension.

    ```ps
    az extension add --source .\dist\mlclassic-1.0.0-py2.py3-none-any.whl
    ```

    If you are upgrading from a previous version of the tool, you can remove the old version using

    ```ps
    az extension remove --name mlclassic
    ```

2. Login with an Azure AD account that has proper permissions to access the ML Classic workspaces, and set the subscription you want to analyze.
   
   ```ps
    az login
    az account list 
    az account set --subscription "Your subscription here"
    ```

3. Run the [automated assessment inventory](./automated-assessment-report.ps1) script. Make sure you set the path to the report file in the `$reportPath` variable.

## Features of the automated assessment tool

1. List all ML Classic workspaces.

    ```ps
    $mlClassicWorkspaces = az resource list --resource-type Microsoft.MachineLearning/Workspaces | ConvertFrom-Json
    ```

2. Get the details of a selected workspace.

    ```ps
    $mlClassicWorkspace = az resource show --ids $mlClassicWorkspaces[0].id | ConvertFrom-Json
    ```

3. Get the workspace id, workspace location, workspace access keys, and API url.

    ```ps
    $mlClassicWorkspaceId = $mlClassicWorkspace.properties.workspaceId
    $mlClassicWorkspaceLocation = $mlClassicWorkspace.location.ToLower().Replace(" ", "")
    $mlClassicWorkspaceKeys = az resource invoke-action --action listworkspacekeys --ids $mlClassicWorkspaces[0].id | ConvertFrom-Json
    $mlClassicApi = $mlClassicWorkspace.properties.studioEndpoint
    ```

4. Get the ML Classic workspace properties

    ```ps
    az mlclassic workspace show -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken
    ```

5. Get the ML classic project in a workspace

    ```ps
    $mlClassicProjects = az mlclassic workspace projects -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json
    ```

6. Get the ML classic experiment id and details

    ```ps
    $mlClassicExperiments = az mlclassic workspace experiments -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json
    $mlClassicExperimentId = $mlClassicExperiments[0].ExperimentId
    $mlClassicExperiment = az mlclassic workspace experiment -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken -eid $mlClassicExperimentId | ConvertFrom-Json
    ```

7. Get the ML classic webservices, webservice id, and webservice details

    ```ps
    $mlClassicWebservices = az mlclassic workspace webservices -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json
    $mlClassicWebserviceId = $mlClassicWebservices[0].Id
    $mlClassicWebservice = az mlclassic workspace webservice -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken -wsid $mlClassicWebserviceId | ConvertFrom-Json
    ```

8. Get the ML classic new webservices, new webservice id, and new webservice details

    ```ps
    $mlClassicNewWebservices = az resource list --resource-type Microsoft.MachineLearning/WebServices | ConvertFrom-Json
    $mlClassicNewWebserviceId = $mlClassicNewWebservices[0].id
    $mlClassicNewWebservice = az resource show --ids $mlClassicNewWebserviceId | ConvertFrom-Json
    ```

9. Get ML classic commitment plans, commitment plan id, commitment plan details, and commitment plan associations

    ```ps
    $mlClassicCommitmentPlans = az resource list --resource-type Microsoft.MachineLearning/CommitmentPlans | ConvertFrom-Json
    $mlClassicCommitmentPlanId = $mlClassicCommitmentPlans[0].id
    $mlClassicCommitmentPlan = az resource show --ids $mlClassicCommitmentPlanId | ConvertFrom-Json
    $mlClassicCommitmentPlanAssociations = (az rest -u "https://management.azure.com$($mlClassicCommitmentPlanId)/commitmentAssociations?api-version=2016-05-01-preview" | ConvertFrom-Json).value
    ```
