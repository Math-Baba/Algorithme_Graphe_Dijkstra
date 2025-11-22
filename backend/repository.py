from database import fetch_all, fetch_one, execute

class GraphRepository:

    def __init__(self):
        # Création du dépôt si absent
        execute("""
            INSERT INTO nodes(name, pos_x, pos_y)
            VALUES ('Depot', 0, 0)
            ON CONFLICT (name) DO NOTHING;
        """)

    def get_graph(self):
        nodes = fetch_all("SELECT * FROM nodes")
        edges = fetch_all("SELECT * FROM edges")

        return {
            "nodes": {n["name"]: {"x": n["pos_x"], "y": n["pos_y"]} for n in nodes},
            "edges": edges
        }

    def create_node(self, name, x, y):
        execute("INSERT INTO nodes(name, pos_x, pos_y) VALUES (%s, %s, %s)", (name, x, y))

    def create_edge(self, a, b, w):
        execute(
            "INSERT INTO edges(node_a, node_b, weight) VALUES (%s, %s, %s)",
            (a, b, w)
        )


    def update_edge_weight(self, a, b, penalty):
        # Ajoute le penalty au poids existant
        execute(
            "UPDATE edges SET weight = weight + %s WHERE node_a = %s AND node_b = %s",
            (penalty, a, b)
        )

def fetch_graph_from_db():
    rows_edges = fetch_all("SELECT node_a, node_b, weight FROM edges")
    graph = {}
    for row in rows_edges:
        a, b, w = row["node_a"], row["node_b"], row["weight"]
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append((b, w))
        graph[b].append((a, w))  # graphe non orienté
    return graph

def fetch_constraints_from_db():
    rows = fetch_all("SELECT node_a, node_b, penalty FROM edges") 
    constraints = {}
    for row in rows:
        a, b, penalty = row["node_a"], row["node_b"], row["penalty"]
        if a not in constraints:
            constraints[a] = {}
        if b not in constraints:
            constraints[b] = {}
        constraints[a][b] = penalty
        constraints[b][a] = penalty  # symétrique
    return constraints