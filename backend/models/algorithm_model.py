class Algorithm:

    @staticmethod
    def Dijkstra(graph, contrainte, source, target):
        if source not in graph or target not in graph:
            return {'distance': float('inf'), 'path': []}
        
        dist = {node: float('inf') for node in graph}
        dist[source] = 0
        previous = {node: None for node in graph}
        unvisited = set(graph.keys())

        while unvisited:
            current = None
            for node in unvisited:
                if current is None or dist[node] < dist[current]:
                    current = node

            if dist[current] == float('inf') or current == target:
                break
            unvisited.remove(current)

            for neighbor, weight in graph[current]:
                if neighbor not in unvisited:
                    continue
                    
                new_dist = dist[current] + weight 
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    previous[neighbor] = current

        path = []
        if dist[target] != float('inf'):
            node = target
            while node is not None:
                path.insert(0, node)
                node = previous[node]

        return {'distance': dist[target], 'path': path}


    @staticmethod
    def Coloriage(graph):
        couleurs = ["rouge", "bleu", "vert", "jaune", "violet", "orange", "rose", "cyan"]
        color_assignment = {}

        for node in graph:
            voisins = [voisin[0] for voisin in graph[node]]
            couleurs_voisins = {color_assignment[v] for v in voisins if v in color_assignment}

            for couleur in couleurs:
                if couleur not in couleurs_voisins:
                    color_assignment[node] = couleur
                    break
        return color_assignment