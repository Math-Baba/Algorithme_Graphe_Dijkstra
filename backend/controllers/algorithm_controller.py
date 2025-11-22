from repository import fetch_constraints_from_db, fetch_graph_from_db
from models.algorithm_model import Algorithm
import json

def handle_dijkstra(data):
    source = data.get("source", "Depot")
    target = data.get("target")
    if not target:
        return {"error": "Target node required"}, 400

    graph = fetch_graph_from_db()          
    contraintes = fetch_constraints_from_db()  

    result = Algorithm.Dijkstra(graph, contraintes, source, target)
    
    if result['distance'] == float('inf'):
        return {"error": "No path found from source to target"}, 404

    return {
        "source": source, 
        "target": target, 
        "distance": result['distance'],
        "path": result['path']
    }


def handle_coloring():
    graph = fetch_graph_from_db()
    result = Algorithm.Coloriage(graph)
    return result