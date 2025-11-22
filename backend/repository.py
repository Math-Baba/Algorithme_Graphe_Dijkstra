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
        constraints = fetch_all("SELECT * FROM constraints")

        constraints_obj = {}
        for c in constraints:
            a = c["node_a"]
            b = c["node_b"]
            p = c["penalty"]

            if a not in constraints_obj:
                constraints_obj[a] = {}
            constraints_obj[a][b] = p

        return {
            "nodes": {n["name"]: {"x": n["pos_x"], "y": n["pos_y"]} for n in nodes},
            "edges": edges,
            "constraints": constraints_obj
        }

    def create_node(self, name, x, y):
        execute("INSERT INTO nodes(name, pos_x, pos_y) VALUES (%s, %s, %s)", (name, x, y))

    def create_edge(self, a, b, w):
        execute("INSERT INTO edges(node_a, node_b, weight) VALUES (%s, %s, %s)", (a, b, w))
        execute("INSERT INTO constraints(node_a, node_b, penalty) VALUES (%s, %s, 0)", (a, b))
        execute("INSERT INTO constraints(node_b, node_a, penalty) VALUES (%s, %s, 0)", (b, a))

    def update_constraint(self, a, b, penalty):
        execute("""
            UPDATE constraints SET penalty = %s
            WHERE node_a = %s AND node_b = %s
        """, (penalty, a, b))

    def block_edge(self, a, b):
        # Bloque totalement le chemin
        execute("""
            UPDATE constraints SET penalty = 999999
            WHERE node_a = %s AND node_b = %s
        """, (a, b))

    def block_node(self, node):
        # Blocage complet du nœud : toutes les arêtes associées deviennent impossibles
        execute("""
            UPDATE constraints SET penalty = 999999
            WHERE node_a = %s OR node_b = %s
        """, (node, node))
