import json
import os

def create_flow_json(flow_id, dest_ip, out_port):
    flow = {
        "flow": [
            {
                "id": str(flow_id),
                "table_id": "0",
                "priority": "100",
                "match": {
                    "ethernet-match": {
                        "ethernet-type": { "type": 2048 }
                    },
                    "ipv4-destination": dest_ip
                },
                "instructions": {
                    "instruction": [
                        {
                            "order": 0,
                            "apply-actions": {
                                "action": [
                                    {
                                        "order": 0,
                                        "dec-nw-ttl": {}
                                    },
                                    {
                                        "order": 1,
                                        "output-action": {
                                            "output-node-connector": str(out_port)
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }
    return flow

def save_flows(path_1_n, path_n_1, port_mapping):
    if not os.path.exists("flows"):
        os.makedirs("flows")
   
    flow_files = []
   
    for i in range(len(path_1_n)):
        current_node = path_1_n[i]
        if i == len(path_1_n) - 1:
            out_port = 1
        else:
            next_node = path_1_n[i+1]
            out_port = port_mapping.get((current_node, next_node))
           
        flow_data = create_flow_json(1, "10.0.2.10/32", out_port)
        filename = "flows/node_%s_forward.json" % current_node
        with open(filename, 'w') as f:
            json.dump(flow_data, f, indent=4)
        flow_files.append((current_node, 1, filename))

    for i in range(len(path_n_1)):
        current_node = path_n_1[i]
        if i == len(path_n_1) - 1:
            out_port = 1
        else:
            next_node = path_n_1[i+1]
            out_port = port_mapping.get((current_node, next_node))

        flow_data = create_flow_json(2, "10.0.1.10/32", out_port)
        filename = "flows/node_%s_reverse.json" % current_node
        with open(filename, 'w') as f:
            json.dump(flow_data, f, indent=4)
        flow_files.append((current_node, 2, filename))

    return flow_files
