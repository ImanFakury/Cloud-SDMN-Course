import networkx as nx

A = [
    [0, 2, 3, 4],
    [2, 0, 0, 1],
    [3, 0, 0, 0],
    [1, 1, 0, 0]
]

def get_paths(matrix):
    n = len(matrix)
    G = nx.DiGraph()

    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                G.add_edge(i+1, j+1, weight=matrix[i][j])

    path_fwd = nx.shortest_path(G, source=1, target=n, weight='weight')
    path_rev = nx.shortest_path(G, source=n, target=1, weight='weight')
    
    return path_fwd, path_rev

if __name__ == '__main__':
    p1, p2 = get_paths(A)
    print("Path 1 -> n:", " -> ".join([f"s{x}" for x in p1]))
    print("Path n -> 1:", " -> ".join([f"s{x}" for x in p2]))
