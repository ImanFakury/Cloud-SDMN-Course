# Virtual Networks based on SDN using ODL

This project explores Software-Defined Networking (SDN) concepts by simulating virtual networks with Mininet and controlling them using the OpenDaylight (ODL) controller[cite: 7, 9, 12]. A detailed write-up of the implementations and results is available in `Report.pdf`[cite: 18].

## Project Structure

This project is divided into four main problems[cite: 18]:

### Problem 1: Mininet and OVS
*   **Objective:** Implement basic LAN topologies and a layer-3 router using Mininet and Open vSwitch (OVS) without an external controller[cite: 9, 11].
*   **Key Files:** Contains Python scripts (`create_net.py`, `create_router_net.py`) to build the topology and shell scripts (`push_flows.sh`, `push_router_flows.sh`) to manually insert OpenFlow rules using `ovs-ofctl`[cite: 19]. Output validation is stored in the `Screenshots` folder[cite: 19].

### Problem 2: OpenDaylight (ODL) Controller
*   **Objective:** Interface with the ODL controller (Nitrogen release) using its RESTCONF API to route traffic dynamically across subnets[cite: 12, 13].
*   **Implementation:** Involves pushing XML/JSON flow payloads via Python scripts to the controller to manage tree and routed topologies[cite: 14].

### Problem 3: Minimum Weight Routing
*   **Objective:** Implement a minimum cost path routing algorithm[cite: 15].
*   **Implementation:** Reads an asymmetric adjacency matrix, calculates the shortest path between end hosts (using algorithms like Dijkstra's), and translates the path into OpenFlow rules pushed to the ODL controller[cite: 15].

### Problem 4: Dynamic Routing (Bonus)
*   **Objective:** Extend the shortest-path routing to handle dynamic link failures[cite: 16].
*   **Implementation:** Actively queries the ODL topology state to monitor link health and recalculates/pushes new flows if an active link goes down[cite: 16].