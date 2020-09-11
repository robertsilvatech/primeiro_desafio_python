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

def logout_vmware():
    token = login_vmware()
    print(token)
    url = ENDPOINT_SESSION
    headers = {
        'Content-Type': 'application/json',
        'vmware-api-session-id': token,
        }
    response = requests.request("DELETE", url, headers=headers, verify=False)
    return response.status_code

def logout_vmware(token):
    url = ENDPOINT_SESSION
    headers = {
        'Content-Type': 'application/json',
        'vmware-api-session-id': token,
        }
    response = requests.delete(url, headers=headers, verify=False)
    return response.status_code

def list_vms(token):
    vms = []
    url = f'https://{server}/rest/vcenter/vm'
    headers = {
        'Content-Type': 'application/json',
        'vmware-api-session-id': token,
        }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        content = response.json()
        for vm in content['value']:
            temp_dict = {}
            vm_id = vm['vm']
            vm_name = vm['name']
            vm_power_state = vm['power_state']
            vm_cpu_count = vm['cpu_count']
            vm_memory_size_mb = vm['memory_size_MiB']
            message = f'ID: {vm_id} - Name: {vm_name} - State: {vm_power_state} - CPU: {vm_cpu_count} - Memory: {vm_memory_size_mb}'
            print(message)
            temp_dict['vm_id'] = vm_id
            temp_dict['vm_name'] = vm_name
            temp_dict['vm_power_state'] = vm_power_state
            temp_dict['vm_cpu_count'] = vm_cpu_count
            temp_dict['vm_memory_size_mb'] = vm_memory_size_mb            
            vms.append(temp_dict)
        return vms
    
def poweroff_vm(token, vmname):
    url = f'https://{server}/rest/vcenter/vm/{vmname}/power/stop'
    headers = {
        'Content-Type': 'application/json',
        'vmware-api-session-id': token,
        }
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:
        message = f'VM {vmname} was stopped'
        return message
    elif response.status_code == 400:
        content = response.json()
        message = content['value']['messages'][0]['default_message']
        return message
    
def poweron_vm(token, vmname):
    url = f'https://{server}/rest/vcenter/vm/{vmname}/power/start'
    headers = {
        'Content-Type': 'application/json',
        'vmware-api-session-id': token,
        }
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:
        message = f'VM {vmname} was started'
        return message
    elif response.status_code == 400:
        content = response.json()
        message = content['value']['messages'][0]['default_message']
        return message

def update_cpu(token, vmname, cpu):
    url = f'https://{server}/rest/vcenter/vm/{vmname}/hardware/cpu'
    headers = {
        'Content-Type': 'application/json',
        'vmware-api-session-id': token,
        }
    data = {
        "spec": {
            "cores_per_socket": cpu,
            "count": cpu,
        }
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data), verify=False)
    print(response)
    print(response.text)
    if response.status_code == 200:
        message = f'VM {vmname} was updated'
        return message
    elif response.status_code == 400:
        content = response.json()
        message = content['value']['messages'][0]['default_message']
        return message