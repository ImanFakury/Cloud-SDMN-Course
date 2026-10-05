#!/bin/bash

echo "--- Pushing simple L2 flows for Switches (s1, s2) ---"

sudo ovs-ofctl -O OpenFlow13 del-flows s1
sudo ovs-ofctl -O OpenFlow13 del-flows s2

sudo ovs-ofctl -O OpenFlow13 add-flow s1 in_port=1,actions=output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s1 in_port=2,actions=output:1

sudo ovs-ofctl -O OpenFlow13 add-flow s2 in_port=1,actions=output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 in_port=2,actions=output:1

echo "--- Pushing L3 routing flows for Router (r1) ---"
sudo ovs-ofctl -O OpenFlow13 del-flows r1


sudo ovs-ofctl -O OpenFlow13 add-flow r1 priority=100,ip,nw_dst=10.0.2.1,actions=mod_dl_src:00:00:00:00:02:FE,mod_dl_dst:00:00:00:00:02:01,dec_ttl,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow r1 priority=100,ip,nw_dst=10.0.1.1,actions=mod_dl_src:00:00:00:00:01:FE,mod_dl_dst:00:00:00:00:01:01,dec_ttl,output:1
echo "--- Flows successfully pushed! ---"
