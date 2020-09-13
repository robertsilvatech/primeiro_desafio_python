import requests
import urllib3
import json
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
server='10.8.100.60'
username = 'administrator@vsphere.local'
password = 'Curso!Zabbix5'

ENDPOINT_SESSION = f'https://{server}/rest/com/vmware/cis/session'

def login_vmware():
    url = ENDPOINT_SESSION
    response = requests.post(url, auth=(username, password), verify=False)
    if response.status_code == 200:
        content = response.json()
        token = content['value']
        return token

token = login_vmware()
vm = 'vm-50'
url = f'https://{server}/rest/vcenter/vm/{vm}'
#query_string = {'filter.names.1': datastore_name}
headers = {
    'Content-Type': 'application/json',
    'vmware-api-session-id': token,
}
response = requests.get(url, headers=headers, verify=False)
if response.status_code == 200:
    content = response.json()
    print(content)