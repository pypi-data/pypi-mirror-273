from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import msal
import requests

'''
Prerequisite: install Azure CLI then login by running "az login"
https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli
'''

# get my personal azure access token
def get_my_token():
    # create a DefaultAzureCredential instance
    credential      = DefaultAzureCredential()
    # get a token
    token           = credential.get_token("https://analysis.windows.net/powerbi/api/.default")
    # extract the access token
    access_token    = token.token
    # use this token for requests on your behalf
    return access_token

'''
Service Principals are also referred to as App Registrations in Azure.

Leveraging service principals, we can store their secrets in a keyvault.
The goal here is to obtain their client id and client secret.
We can use this information to obtain bearer authentication token for a service principal.
'''

def get_secret_value(subscription_id, key_vault_name, secret_name):
    subscription_id = subscription_id
    key_vault_name  = key_vault_name
    secret_name     = secret_name
    key_vault_uri   = f"https://{key_vault_name}.vault.azure.net"
    client          = SecretClient(vault_url=key_vault_uri,credential=DefaultAzureCredential(),subscription_id=subscription_id)
    client_secret   = client.get_secret(secret_name).value
    return client_secret


def get_service_principal_access_token(tenant_id, client_id, client_secret):
    # Power BI Authentication
    authority       = f"https://login.microsoft.com/{tenant_id}"
    scopes          = ["https://analysis.windows.net/powerbi/api/.default"]
    app             = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    result          = app.acquire_token_for_client(scopes=scopes)
    access_token    = result['access_token']
    return access_token


#================================================================
# Get Workspace ID by Name
#================================================================
def get_workspace_id(access_token, workspace_name):
    groupId = ""
    url = "https://api.powerbi.com/v1.0/myorg/groups"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    workspaces = response.json()['value']
    for workspace in workspaces:
        if workspace['name'] == workspace_name:
            groupId = workspace['id']
    return groupId

#================================================================
# Get or create workspace
# Get workspace id, if it exists
# If the workspace does not exist, create one and return the id
#================================================================
def get_or_create_workspace(access_token, workspace_name):
    groupId = get_workspace_id(access_token, workspace_name)
    if groupId =='':
        url = 'https://api.powerbi.com/v1.0/myorg/groups'
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": workspace_name
        }
        response = requests.post(url, headers=headers, json=payload)
        groupId = response.json()['id']
    else:
        pass
    return groupId