if ((az extension list --query "[?name=='mlclassic']" | ConvertFrom-Json ).Count -eq 1)
{
    Write-Output 'Removing Azure ML Classic CLI extension...'
    az extension remove --name mlclassic
}

Write-Output 'Adding latest version of the Azure ML Classic CLI extension...'
az extension add --source .\automated_assessment\dist\mlclassic-1.0.0-py2.py3-none-any.whl --yes

# define the path to save the report. replace with your own path
$reportPath = "D:\Git\microsoft-ml\subscription-1.json"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# WARNING: Setting the following variable to $true will instruct the script to extract all
# information, including sensitive details like storage keys and workspace keys. Make sure
# you protect properly the resulting report file.
#
# ----------------------------------------------------------------------------------------
$verbose = $true

$subscription = az account show | ConvertFrom-Json
$report = @{
    "subscription" = @{
        "id" = $subscription.id
        "name" = $subscription.name
    }
    "workspaces" = @()
    "newwebservices" = @()
    "commitmentplans" = @()
}

Write-Output "Retrieving the list of Azure ML classic workspaces..."
$mlClassicWorkspaces = az resource list --resource-type Microsoft.MachineLearning/Workspaces | ConvertFrom-Json
if ($mlClassicWorkspaces) {

    Write-Output "Found $($mlClassicWorkspaces.Count) Azure ML classic workspaces."
    foreach ($wks in $mlClassicWorkspaces) {

        $mlClassicWorkspace = az resource show --ids $wks.id | ConvertFrom-Json
        $mlClassicWorkspaceId = $mlClassicWorkspace.properties.workspaceId
        $mlClassicWorkspaceName = $wks.name
        $mlClassicWorkspaceLocation = $wks.location
        $mlClassicApi = $mlClassicWorkspace.properties.studioEndpoint

        Write-Output "Processing workspace $($mlClassicWorkspaceName) from $($mlClassicWorkspaceLocation) using $($mlClassicApi)..."

        $mlClassicWorkspaceKeys = az resource invoke-action --action listworkspacekeys --ids $wks.id | ConvertFrom-Json
        $mlClassicWorkspaceDetails = az mlclassic workspace show -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json

        $workspace = @{
            "id" = $mlClassicWorkspaceId
            "name" = $mlClassicWorkspaceName
            "location" = $mlClassicWorkspaceLocation
            "api" = $mlClassicApi
            "projects" = @()
            "experiments" = @()
            "datasources" = @()
            "webservices" = @()
            "webservicegroups" = @()
        }

        if ($verbose) {
            $workspace["info"] = $mlClassicWorkspace
            $workspace["details"] = $mlClassicWorkspaceDetails
        }

        Write-Output "Retrieving the list of projects..."
        $mlClassicProjects = az mlclassic workspace projects -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json

        if ($mlClassicProjects) {

            Write-Output "Found $($mlClassicProjects.Count) projects."

            foreach ($prj in $mlClassicProjects) {

                $project = @{
                    "name" = $prj.name 
                }

                if ($verbose) {
                    $project["info"] = $prj
                }

                $workspace["projects"] += $project
            }
        } else {
            Write-Output "No projects were found."
        }

        Write-Output "Retrieving the list of experiments..."
        $mlClassicExperiments = az mlclassic workspace experiments -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json

        if ($mlClassicExperiments) {
            
            Write-Output "Found $($mlClassicExperiments.Count) experiments."
            
            foreach ($exp in $mlClassicExperiments) {

                if ($exp.Category -ne "user") {
                    # Write-Output "Skipping experiment $($exp.Description) ($($exp.ExperimentId)) because its category is $($exp.Category)"
                    continue
                }

                Write-Output "Processing experiment $($exp.Description) ($($exp.ExperimentId))..."
                $mlClassicExperimentId = $exp.ExperimentId
                $mlClassicExperiment = az mlclassic workspace experiment -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken -eid $mlClassicExperimentId | ConvertFrom-Json

                $experiment = @{
                    "id" = $exp.ExperimentId
                    "description" = $exp.Description
                    "category" = $exp.Category
                }

                if ($verbose) {
                    $experiment["info"] = $exp
                    $experiment["details"] = $mlClassicExperiment
                }

                $workspace["experiments"] += $experiment
            }
        } else {
            Write-Output "No experiments were found."
        }

        Write-Output "Retrieving the list of datasources..."
        $mlClassicDatasources = az mlclassic workspace datasources -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json

        if ($mlClassicDatasources) {

            Write-Output "Found $($mlClassicDatasources.Count) datasources."

            foreach ($ds in $mlClassicDatasources) {

                if ($ds.Owner -eq "Microsoft Corporation") {
                    # Write-Output "Skipping datasource $($ds.Name) ($($ds.Id)) because its owner is $($ds.Owner)"
                    continue
                }

                Write-Output "Processing datasource $($ds.Name) ($($ds.Id))..."
                $datasource = @{
                    "id" = $ds.Id
                    "name" = $ds.Name
                }

                if ($verbose) {
                    $datasource["info"] = $ds
                }

                $workspace["datasources"] += $ds
            }
        } else {
            Write-Output "No datasources were found."
        }

        Write-Output "Retrieving the list of classic webservices..."
        $mlClassicWebservices = az mlclassic workspace webservices -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json
        if ($mlClassicWebservices) {
            Write-Output "Found $($mlClassicWebservices.Count) classic webservices."
            if ($verbose) {
                foreach ($ws in $mlClassicWebservices) {
                    $workspace["webservices"] += $ws
                }
            }
        } else {
            Write-Output "No classic webservices were found."
        }

        Write-Output "Retrieving the list of classic webservice groups..."
        $mlClassicWebserviceGroups = az mlclassic workspace webservicegroups -wid $mlClassicWorkspaceId -wl $mlClassicWorkspaceLocation -wapi $mlClassicApi -wat $mlClassicWorkspaceKeys.primaryToken | ConvertFrom-Json
        if ($mlClassicWebserviceGroups) {
            Write-Output "Found $($mlClassicWebserviceGroups.Count) classic webservice groups."
            if ($verbose) {
                foreach ($wsg in $mlClassicWebserviceGroups) {
                    $workspace["webservicegroups"] += $wsg
                }
            }
        } else {
            Write-Output "No classic webservice groups were found."
        }

        $report["workspaces"] += $workspace
    }
} else {

    Write-Output "Could not find any Azure ML classic workspaces."
}

Write-Output "Retrieving the list of Azure ML classic new webservices..."
$mlClassicNewWebservices = az resource list --resource-type Microsoft.MachineLearning/WebServices | ConvertFrom-Json
if ($mlClassicNewWebservices) {
    Write-Output "Found $($mlClassicNewWebservices.Count) Azure ML classic new webservices."
    $report["newwebservices"] = $mlClassicNewWebservices
} else {
    Write-Output "No Azure ML classic new webservices were found."
}

Write-Output "Retrieving the list of Azure ML classic commitment plans..."
$mlClassicCommitmentPlans = az resource list --resource-type Microsoft.MachineLearning/CommitmentPlans | ConvertFrom-Json
if ($mlClassicCommitmentPlans) {

    Write-Output "Found $($mlClassicCommitmentPlans.Count) Azure ML classic commitment plans."
    
    foreach ($cp in $mlClassicCommitmentPlans) {

        Write-Output "Processing commitment plan $($cp.Name) ($($cp.Id))..."
        $commitmentPlan = @{
            "id" = $cp.id
            "name" = $cp.name
            "location" = $cp.location
            "associations" = @()
        }

        if ($verbose) {
            $commitmentPlan["info"] = $cp
        }

        Write-Output "Retrieving the list of commitment plan associations..."
        $mlClassicCommitmentPlanAssociations = (az rest -u "https://management.azure.com$($cp.id)/commitmentAssociations?api-version=2016-05-01-preview" | ConvertFrom-Json).value

        if ($mlClassicCommitmentPlanAssociations) {
            Write-Output "Found $($mlClassicCommitmentPlanAssociations.Count) commitment plan associations."
            $commitmentPlan["associations"] = $mlClassicCommitmentPlanAssociations
        } else {
            Write-Output "No commitment plan associations were found."
        }

        $report["commitmentplans"] += $commitmentPlan
    }
} else {
    Write-Output "No Azure ML classic commitment plans were found."
}

$report | ConvertTo-Json -Depth 100 | Out-File $reportPath

