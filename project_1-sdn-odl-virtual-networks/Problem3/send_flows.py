import os
import json
import requests

ODL_IP = "127.0.0.1"
ODL_PORT = "8181"
AUTH = ('admin', 'admin')
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
flow_dir = 'flows'

print("--- Sending Minimum Weight Flows to OpenDaylight ---")

for filename in os.listdir(flow_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(flow_dir, filename)
        
        parts = filename.split('_')
        node_id = parts[1]
        flow_id = parts[3].split('.')[0]
        
        url = f"http://{ODL_IP}:{ODL_PORT}/restconf/config/opendaylight-inventory:nodes/node/openflow:{node_id}/table/0/flow/{flow_id}"
        
        with open(filepath, 'r') as f:
            flow_data = json.load(f)
            
        response = requests.put(url, auth=AUTH, headers=HEADERS, json=flow_data)
        
        if response.status_code in [200, 201]:
            print(f"SUCCESS: Pushed {filename} to openflow:{node_id}")
        else:
            print(f"FAILED: {filename}. Status Code: {response.status_code}")
