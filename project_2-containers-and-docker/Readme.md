# Containers and Docker

This project focuses on the foundational technologies behind containerization, covering Linux network namespaces, custom runtime execution, and Dockerizing a web service.

## Project Structure

The assignment is organized into three specific problems:

### Problem 1: Container Networking
*   **Objective:** Create an isolated network topology using raw Linux network namespaces, virtual Ethernet pairs, and bridges.
*   **Key Files:** Contains `setup_topology.sh` to initialize the bridged network and router namespaces, and `ping_nodes.sh` to verify connectivity across subnets.
*   **Documentation:** Includes `figure2_explanation.md` and `figure3_explanation.md` detailing theoretical routing rules for disjoint bridges and cross-server namespace communication. 

### Problem 2: Container Runtime
*   **Objective:** Build a custom, lightweight container runtime CLI.
*   **Implementation:** The CLI accepts a hostname parameter and isolates the process by creating new `net`, `mnt`, `pid`, and `uts` namespaces. It mounts an isolated Ubuntu 20.04 root filesystem so that the initial bash process runs as PID 1 inside the container.

### Problem 3: Dockerizing an HTTP Server
*   **Objective:** Develop a stateful web server and package it as a Docker image.
*   **Implementation:** The server exposes an `/api/v1/status` endpoint handling both GET and POST requests. The solution includes the application source code and a `Dockerfile` for building and exposing the service on the host network.