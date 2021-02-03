---
page_type: sample
languages:
- yaml
- python
products:
- azure
- azure-devops
- azure-container-instance
extensions:
  services: Containerinstance
name: Performance Testing with K6 and ACI
description: "Automate performace tests using K6 and Azure Container Instance."
urlFragment: "k6-aci"
---
# Performance Testing with K6 and ACI

This sample code briefly describes how to use [K6](https://k6.io) performance testing tool to execute tests in Azure Container Instance(ACI). 

## Prerequisites

You should have the following tools installed:

* Shell
* [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* [Azure DevOps CLI extension](https://docs.microsoft.com/en-us/azure/devops/cli/?view=azure-devops)
* [jq](https://stedolan.github.io/jq/download/)

You should have the following Azure resources:

* [Azure DevOps Project](https://docs.microsoft.com/en-us/azure/devops/organizations/projects/create-project?view=azure-devops&tabs=preview-page)
* [Azure Container Registry (ACR)](https://azure.microsoft.com/en-us/services/container-registry/) with Admin user enabled

## Getting Started

### 1. Importing this repository to Azure DevOps

Log in to Azure through Azure CLI:

```sh
az login
```

> NOTE: Make sure you are using the correct subscription. You can use `az account show` to display what is the current selected one and [`az account set`](https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-set) to change it.

Configure Azure DevOps CLI with your organization/project settings:

```shell
ORGANIZATION_URL=https://dev.azure.com/your-organization
PROJECT_NAME=YourProject

az devops configure --defaults organization=$ORGANIZATION_URL project=$PROJECT_NAME
```

Import this repository on your Azure DevOps project:

```shell
REPOSITORY_NAME=k6-load-test-with-aci
REPOSITORY_URL=https://github.com/Azure-Samples/k6-load-test-with-aci

az repos create --name $REPOSITORY_NAME
az repos import create --git-source-url $REPOSITORY_URL --repository $REPOSITORY_NAME
```

### 2. Configuring Azure credentials

Create an [Azure service principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals#service-principal-object):

```shell
SERVICE_PRINCIPAL_NAME=AzureServicePrincipal

SERVICE_PRINCIPAL=$(az ad sp create-for-rbac --name $SERVICE_PRINCIPAL_NAME)
```

Run the following commands to fill the credentials variables:

```shell
CLIENT_ID=$(echo $SERVICE_PRINCIPAL | jq -r .appId)
CLIENT_SECRET=$(echo $SERVICE_PRINCIPAL | jq -r .password)
TENANT_ID=$(echo $SERVICE_PRINCIPAL | jq -r .tenant)
SUBSCRIPTION_ID=$(az account show | jq -r .id)
SUBSCRIPTION_NAME=$(az account show | jq -r .name)
```

Create an Azure [service connection](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml) on Azure DevOps:

```shell
SERVICE_CONNECTION_NAME=AzureServiceConnection

export AZURE_DEVOPS_EXT_AZURE_RM_SERVICE_PRINCIPAL_KEY=$CLIENT_SECRET

SERVICE_ENDPOINT_ID=$(az devops service-endpoint azurerm create --azure-rm-service-principal-id $CLIENT_ID \
                        --azure-rm-subscription-id $SUBSCRIPTION_ID --azure-rm-subscription-name $SUBSCRIPTION_NAME  \
                        --azure-rm-tenant-id $TENANT_ID --name $SERVICE_CONNECTION_NAME | jq -r .id)

az devops service-endpoint update --id $SERVICE_ENDPOINT_ID --enable-for-all true
```

### 3. Creating and Running the Docker Pipeline

```shell
PIPELINE_NAME_DOCKER=sample-app-build

az pipelines create --name $PIPELINE_NAME_DOCKER --repository $REPOSITORY_NAME \
    --repository-type tfsgit --branch main \
    --yml-path pipelines/azure-pipelines.docker.yml
```

### 4. Creating the K6 Pipeline

```shell
PIPELINE_NAME_K6=k6-load-test

az pipelines create --name $PIPELINE_NAME_K6 --repository $REPOSITORY_NAME \
    --repository-type tfsgit --branch main --skip-first-run \
    --yml-path pipelines/azure-pipelines.load-test.yml
```

## The K6 test application docker image


## Creating tests scripts


## Deploying to ACI


## Publishing test results to Azure DevOps
