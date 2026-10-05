import json
import os
from spf import get_paths, A

n = len(A)
path_fwd, path_rev = get_paths(A)

if not os.path.exists('flows'):
    os.makedirs('flows')

def write_flow(node, flow_id, data):
    filename = f"flows/node_{node}_flow_{flow_id}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def gen_l3_flow(flow_id, dst_ip, src_mac, dst_mac, out_port):
    return {
        "flow": [{
            "id": str(flow_id), "table_id": 0, "priority": 100,
            "match": {
                "ethernet-match": { "ethernet-type": { "type": 2048 } },
                "ipv4-destination": dst_ip
            },
            "instructions": { "instruction": [{ "order": 0,
                "apply-actions": { "action": [
                    { "order": 0, "set-dl-src-action": { "address": src_mac } },
                    { "order": 1, "set-dl-dst-action": { "address": dst_mac } },
                    { "order": 2, "dec-nw-ttl": {} },
                    { "order": 3, "output-action": { "output-node-connector": str(out_port) } }
                ]}
            }]}
        }]
    }

def gen_fwd_flow(flow_id, dst_ip, out_port):
    return {
        "flow": [{
            "id": str(flow_id), "table_id": 0, "priority": 50,
            "match": {
                "ethernet-match": { "ethernet-type": { "type": 2048 } },
                "ipv4-destination": dst_ip
            },
            "instructions": { "instruction": [{ "order": 0,
                "apply-actions": { "action": [
                    { "order": 0, "output-action": { "output-node-connector": str(out_port) } }
                ]}
            }]}
        }]
    }

print("--- Generating ODL RESTCONF Payloads based on Shortest Path ---")
flow_counters = {i: 1 for i in range(1, n+1)}

dst_ip_fwd = "10.0.2.1/32"
for idx, node in enumerate(path_fwd):
    if idx == 0:
        out_p = path_fwd[idx+1]
        flow = gen_l3_flow(flow_counters[node], dst_ip_fwd, "00:00:00:00:02:fe", "00:00:00:00:02:01", out_p)
    elif idx == len(path_fwd) - 1:
        out_p = n + 1 
        flow = gen_fwd_flow(flow_counters[node], dst_ip_fwd, out_p)
    else:
        out_p = path_fwd[idx+1]
        flow = gen_fwd_flow(flow_counters[node], dst_ip_fwd, out_p)
    
    write_flow(node, flow_counters[node], flow)
    flow_counters[node] += 1

dst_ip_rev = "10.0.1.1/32"
for idx, node in enumerate(path_rev):
    if idx == 0:
        out_p = path_rev[idx+1]
        flow = gen_l3_flow(flow_counters[node], dst_ip_rev, "00:00:00:00:01:fe", "00:00:00:00:01:01", out_p)
    elif idx == len(path_rev) - 1:
        out_p = n + 1 
        flow = gen_fwd_flow(flow_counters[node], dst_ip_rev, out_p)
    else:
        out_p = path_rev[idx+1]
        flow = gen_fwd_flow(flow_counters[node], dst_ip_rev, out_p)
    
    write_flow(node, flow_counters[node], flow)
    flow_counters[node] += 1

print(f"All flows generated in 'flows/' directory.")
