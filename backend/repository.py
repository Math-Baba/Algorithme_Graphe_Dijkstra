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

    def edge_exists(self, a, b):
        """Vérifie si une arête existe déjà entre deux nœuds (dans les deux sens car graphe non orienté)"""
        result = fetch_one(
            "SELECT COUNT(*) as count FROM edges WHERE (node_a = %s AND node_b = %s) OR (node_a = %s AND node_b = %s)",
            (a, b, b, a)
        )
        return result["count"] > 0 if result else False

    def create_edge(self, a, b, w):
        # Vérifier si l'arête existe déjà
        if self.edge_exists(a, b):
            raise ValueError(f"Une arête existe déjà entre les nœuds '{a}' et '{b}'")
        
        execute(
            "INSERT INTO edges(node_a, node_b, weight) VALUES (%s, %s, %s)",
            (a, b, w)
        )


    def get_edge_weight(self, a, b):
        """Récupère le poids actuel d'une arête (dans les deux sens car graphe non orienté)"""
        result = fetch_one(
            "SELECT weight FROM edges WHERE (node_a = %s AND node_b = %s) OR (node_a = %s AND node_b = %s) LIMIT 1",
            (a, b, b, a)
        )
        return result["weight"] if result else None

    def update_edge_weight(self, a, b, penalty):
        # Vérifier si l'arête existe
        if not self.edge_exists(a, b):
            raise ValueError(f"Aucune arête n'existe entre les nœuds '{a}' et '{b}'")
        
        # Récupérer le poids actuel
        current_weight = self.get_edge_weight(a, b)
        if current_weight is None:
            raise ValueError(f"Impossible de récupérer le poids de l'arête entre '{a}' et '{b}'")
        
        # Vérifier que le nouveau poids ne sera pas négatif
        new_weight = current_weight + penalty
        if new_weight < 0:
            raise ValueError(f"Le poids ne peut pas être négatif. Poids actuel: {current_weight}, pénalité: {penalty}, résultat: {new_weight}")
        
        # Ajouter le penalty au poids existant
        execute(
            "UPDATE edges SET weight = weight + %s WHERE (node_a = %s AND node_b = %s) OR (node_a = %s AND node_b = %s)",
            (penalty, a, b, b, a)
        )

    def delete_node(self, name):
        # Supprimer d'abord toutes les arêtes liées au nœud, puis le nœud
        execute("DELETE FROM edges WHERE node_a = %s OR node_b = %s", (name, name))
        execute("DELETE FROM nodes WHERE name = %s", (name,))

    def delete_edge(self, a, b):
        # Supprimer l'arête (dans les deux sens car graphe non orienté)
        execute(
            "DELETE FROM edges WHERE (node_a = %s AND node_b = %s) OR (node_a = %s AND node_b = %s)",
            (a, b, b, a)
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