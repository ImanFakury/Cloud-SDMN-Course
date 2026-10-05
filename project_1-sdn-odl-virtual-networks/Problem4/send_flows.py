import requests
import json

ODL_IP = "127.0.0.1"
AUTH = ('admin', 'admin')
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}

def push_flow_to_odl(node_id, flow_id, json_file_path):
    url = "http://%s:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:%s/table/0/flow/%s" % (ODL_IP, node_id, flow_id)
   
    with open(json_file_path, 'r') as f:
        flow_data = json.load(f)
       
    try:
        response = requests.put(url, auth=AUTH, headers=HEADERS, json=flow_data)
        if response.status_code in [200, 201]:
            print("Successfully pushed flow %s to openflow:%s" % (flow_id, node_id))
        else:
            print("Failed to push flow. Status: %s. Resp: %s" % (response.status_code, response.text))
    except Exception as e:
        print("RESTCONF connection error: %s" % e)
