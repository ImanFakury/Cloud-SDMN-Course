import json
import os

if not os.path.exists('flows'):
    os.makedirs('flows')

def write_flow(node, flow_id, data):
    filename = f"flows/node_{node}_flow_{flow_id}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Created: {filename}")

def gen_l2_flow(flow_id, in_port, out_port):
    return {
        "flow": [{
            "id": str(flow_id), "table_id": 0, "priority": 100,
            "match": { "in-port": str(in_port) },
            "instructions": { "instruction": [{ "order": 0,
                "apply-actions": { "action": [{ "order": 0,
                    "output-action": { "output-node-connector": str(out_port) }
                }]}
            }]}
        }]
    }

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

print("--- Generating ODL RESTCONF Payloads ---")

write_flow("1", "1", gen_l2_flow("1", "1", "2"))
write_flow("1", "2", gen_l2_flow("2", "2", "1"))

write_flow("2", "1", gen_l2_flow("1", "1", "2"))
write_flow("2", "2", gen_l2_flow("2", "2", "1"))

write_flow("3", "1", gen_l3_flow("1", "10.0.2.1/32", "00:00:00:00:02:fe", "00:00:00:00:02:01", "2"))
write_flow("3", "2", gen_l3_flow("2", "10.0.1.1/32", "00:00:00:00:01:fe", "00:00:00:00:01:01", "1"))

print("All flows successfully saved to the 'flows/' folder.")
