#!/bin/bash

echo "--- Pushing flows to s1 ---"
sudo ovs-ofctl -O OpenFlow13 del-flows s1
sudo ovs-ofctl -O OpenFlow13 add-flow s1 in_port=1,actions=output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s1 in_port=2,actions=output:1
echo "--- Flows successfully pushed! ---"
echo "Current flows in s1:"
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
