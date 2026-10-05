import time
import os
import requests
from spf import calculate_spf
from create_flows import save_flows
from send_flows import push_flow_to_odl

A = [
    [0, 2, 3, 4],
    [2, 0, 0, 1],
    [3, 0, 0, 0],
    [1, 1, 0, 0]
]
N_NODES = len(A)
ODL_IP = "127.0.0.1"
AUTH = ('admin', 'admin')

port_counters = {i+1: 1 for i in range(N_NODES)}
port_counters[1] += 1
port_counters[N_NODES] += 1

expected_links = []
port_mapping = {}

for i in range(N_NODES):
    for j in range(i+1, N_NODES):
        if A[i][j] > 0 or A[j][i] > 0:
            src = i + 1
            dst = j + 1
            src_port = port_counters[src]
            dst_port = port_counters[dst]
           
            expected_links.append((src, dst, src_port, dst_port))
            port_mapping[(src, dst)] = src_port
            port_mapping[(dst, src)] = dst_port
           
            port_counters[src] += 1
            port_counters[dst] += 1

def get_inventory():
    url = "http://%s:8181/restconf/operational/opendaylight-inventory:nodes/" % ODL_IP
    try:
        resp = requests.get(url, auth=AUTH, headers={'Accept': 'application/json'})
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

def monitor_network():
    last_path_1_n = None
    last_path_n_1 = None
   
    print("Starting bulletproof inventory watcher...")
   
    while True:
        inventory = get_inventory()
        if not inventory or 'nodes' not in inventory:
            time.sleep(5)
            continue
           
        nodes = inventory.get('nodes', {}).get('node', [])
        if not nodes:
            time.sleep(5)
            continue
           
        port_states = {}
        for node in nodes:
            try:
                node_id = int(node['id'].split(':')[1], 16)
                port_states[node_id] = {}
                for nc in node.get('node-connector', []):
                    port_num = nc.get('flow-node-inventory:port-number')
                    state = nc.get('flow-node-inventory:state', {})
                    is_down = state.get('link-down', False)
                    port_states[node_id][str(port_num)] = is_down
            except:
                continue
               
        active_links = []
        for src, dst, src_port, dst_port in expected_links:
            src_down = port_states.get(src, {}).get(str(src_port), True)
            dst_down = port_states.get(dst, {}).get(str(dst_port), True)
           
            if not src_down and not dst_down:
                active_links.append((src, dst))
                active_links.append((dst, src))
               
        if not active_links:
            time.sleep(5)
            continue
           
        path_1_n, path_n_1 = calculate_spf(A, active_links, N_NODES)
       
        if path_1_n and path_n_1 and (path_1_n != last_path_1_n or path_n_1 != last_path_n_1):
            print("\n=================================")
            print("Topology Change Detected!")
            print("New Route H1 -> H4:", path_1_n)
            print("New Route H4 -> H1:", path_n_1)
            print("Pushing OpenFlow rules...")
            print("=================================\n")
           
            # CLEAR PREVIOUS FLOWS TO PREVENT CONFLICTS
            os.system(f"curl -s -u admin:admin -X DELETE http://{ODL_IP}:8181/restconf/config/opendaylight-inventory:nodes > /dev/null")
            time.sleep(1) # Wait a second for controller to digest deletion
           
            flow_files = save_flows(path_1_n, path_n_1, port_mapping)
            for node, flow_id, filepath in flow_files:
                push_flow_to_odl(node, flow_id, filepath)
               
            last_path_1_n = path_1_n
            last_path_n_1 = path_n_1
           
        time.sleep(5)

if __name__ == "__main__":
    monitor_network()
