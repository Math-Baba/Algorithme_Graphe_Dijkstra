class Graph: 
    def init_graph():
        # Initialise un graphe vide avec un dépôt 
        graph = {"Depot": []}
        constraints = {"Depot": {}}
        return graph, constraints

    def Dijkstra(graph, contrainte, source):
        dist = {node: float('inf') for node in graph}
        dist[source] = 0
        unvisited = set(graph.keys())

        while unvisited:
            current = None
            for node in unvisited:
                if current is None or dist[node] < dist[current]:
                    current = node

            if dist[current] == float('inf'):
                break
            unvisited.remove(current)

            for neighbor, weight in graph[current]:
                new_dist = dist[current] + weight + contrainte[current][neighbor]
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
        print(dist)

    # graph = {
    #     'A': [('B', 2), ('C', 5)],
    #     'B': [('A', 2), ('C', 1), ('D', 4)],
    #     'C': [('A', 5), ('B', 1), ('D', 2)],
    #     'D': [('B', 4), ('C', 2)]
    # }

    # contrainte = {
    #     'A': {'B': 7, 'C': 0},
    #     'B': {'A': 7, 'C': 0, 'D': 0},
    #     'C': {'A': 0, 'B': 0, 'D': 0},
    #     'D': {'B': 0, 'C': 0}
    # }

    # Dijkstra(graph, contrainte, 'A')

    def Coloriage(graph):
        degres = {node: len(graph[node]) for node in graph}
        deg_max = max(degres.values())
        print(degres)
        print(deg_max)

        couleurs = ["rouge", "bleu", "vert", "jaune", "violet", "orange", "rose", "cyan"]
        color_assignment = {}

        for node in graph:
            voisins = []
            for element in graph[node]:
                voisin = element[0]
                voisins.append(voisin)

            couleurs_voisins = set()
            for voisin in voisins:
                if voisin in color_assignment:
                    couleur_du_voisin = color_assignment[voisin]
                    couleurs_voisins.add(couleur_du_voisin)

            for couleur in couleurs:
                if couleur not in couleurs_voisins:
                    color_assignment[node] = couleur
                    break

        print(color_assignment)
    # Coloriage(graph)
    
    def add_node(graph, constraints, node_name):
        if node_name in graph:
            print(f"Le noeud {node_name} existe déjà.")
            return

        graph[node_name] = []
        constraints[node_name] = {}

        # Chaque autre noeud doit avoir une contrainte vers lui
        for existing in graph:
            if existing != node_name:
                constraints[existing][node_name] = 0
                constraints[node_name][existing] = 0

        print(f"Noeud {node_name} ajouté.")

    def add_edge(graph, constraints, node_a, node_b, weight):
        # Vérification minimale
        if node_a not in graph or node_b not in graph:
            print("Un des noeuds n'existe pas.")
            return

        # Ajouter l’arête dans les deux sens (graphe non orienté)
        graph[node_a].append((node_b, weight))
        graph[node_b].append((node_a, weight))

        print(f"Arête ajoutée : {node_a} ---{weight}--- {node_b}")
    
