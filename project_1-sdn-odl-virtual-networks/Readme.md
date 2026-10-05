# Virtual Networks based on SDN using ODL

This project explores Software-Defined Networking (SDN) concepts by simulating virtual networks with Mininet and controlling them using the OpenDaylight (ODL) controller. A detailed write-up of the implementations and results is available in `Report.pdf`.

## Project Structure

This project is divided into four main problems:

### Problem 1: Mininet and OVS
*   **Objective:** Implement basic LAN topologies and a layer-3 router using Mininet and Open vSwitch (OVS) without an external controller.
*   **Key Files:** Contains Python scripts (`create_net.py`, `create_router_net.py`) to build the topology and shell scripts (`push_flows.sh`, `push_router_flows.sh`) to manually insert OpenFlow rules using `ovs-ofctl`. Output validation is stored in the `Screenshots` folder.

### Problem 2: OpenDaylight (ODL) Controller
*   **Objective:** Interface with the ODL controller (Nitrogen release) using its RESTCONF API to route traffic dynamically across subnets.
*   **Implementation:** Involves pushing XML/JSON flow payloads via Python scripts to the controller to manage tree and routed topologies.

### Problem 3: Minimum Weight Routing
*   **Objective:** Implement a minimum cost path routing algorithm.
*   **Implementation:** Reads an asymmetric adjacency matrix, calculates the shortest path between end hosts (using algorithms like Dijkstra's), and translates the path into OpenFlow rules pushed to the ODL controller.

### Problem 4: Dynamic Routing (Bonus)
*   **Objective:** Extend the shortest-path routing to handle dynamic link failures.
*   **Implementation:** Actively queries the ODL topology state to monitor link health and recalculates/pushes new flows if an active link goes down.