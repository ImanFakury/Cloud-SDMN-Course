import networkx as nx

def calculate_spf(A, active_links, n):
    G = nx.DiGraph()
    G.add_nodes_from(range(1, n + 1))
   
    for i in range(n):
        for j in range(n):
            if A[i][j] > 0:
                if (i+1, j+1) in active_links:
                    G.add_edge(i+1, j+1, weight=A[i][j])

    try:
        path_1_n = nx.shortest_path(G, source=1, target=n, weight='weight')
    except nx.NetworkXNoPath:
        path_1_n = []
       
    try:
        path_n_1 = nx.shortest_path(G, source=n, target=1, weight='weight')
    except nx.NetworkXNoPath:
        path_n_1 = []

    return path_1_n, path_n_1
