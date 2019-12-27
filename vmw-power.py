#!/usr/bin/env python3
import requests
import urllib3
import sys
from urllib3.exceptions import InsecureRequestWarning

'''Variable Initiation'''

ip_addr = '127.0.0.1:8697'  #change ip:port to what VMW REST API is showing
machine_list = ['k8s-master','k8s-worker1','k8s-worker2','k8s-worker3']
authCode = 'YOUR_AUTH_TOKEN_HERE'

'''action - on, off, shutdown, suspend, pause, unpause'''
acceptable_actions = ['on', 'off', 'shutdown', 'suspend', 'pause', 'unpause']
try:
    sys.argv[1]
except NameError:
        action = "on"
else:
    if sys.argv[1] in acceptable_actions:
        action = sys.argv[1]
    else:
        print("ERROR: Action must be: on, off, shutdown, suspend, pause, or unpause")
        exit()


urllib3.disable_warnings(category=InsecureRequestWarning)
resp = requests.get(url='https://' + ip_addr + '/api/vms', headers={'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + authCode}, verify=False)
if resp.status_code != 200:
    #something fell down
    print("Status Code " + resp.status_code + ": Something bad happened")
result_json = resp.json()

for todo_item in resp.json():
    current_id = todo_item['id']
    current_path = todo_item['path']
    for machine in machine_list:
        if current_path.find(machine) > -1:
            print(machine + ': ' + current_id)    
            urllib3.disable_warnings(category=InsecureRequestWarning)
            current_url = 'https://' + ip_addr + '/api/vms/' + current_id + '/power'
            resp = requests.put(current_url, data=action, headers={'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json', 'Accept': 'application/vnd.vmware.vmw.rest-v1+json', 'Authorization': 'Basic ' + authCode}, verify=False)
            print(resp.text) #feel free to put more exception code here

