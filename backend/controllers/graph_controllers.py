import json
from repository import GraphRepository

repo = GraphRepository()

def handle_get_graph():
    return repo.get_graph()

def handle_post_node(body):
    data = json.loads(body)
    name = data.get("name")
    x = data.get("x", 0)
    y = data.get("y", 0)

    if not name:
        return '{"error":"Missing name"}', 400

    repo.create_node(name, x, y)
    return '{"message":"Node added"}', 201

def handle_post_edge(body_text):
    data = json.loads(body_text)
    a = data.get("node_a")
    b = data.get("node_b")
    w = data.get("weight", 1)

    repo.create_edge(a, b, w)
    return json.dumps({"message": "Edge created"}), 201

def handle_post_constraint(body_text):
    data = json.loads(body_text)
    a = data.get("node_a")
    b = data.get("node_b")
    penalty = data.get("penalty", 0)

    repo.update_edge_weight(a, b, penalty)
    return json.dumps({"message": "Edge weight updated"}), 200

def handle_block_edge(body):
    data = json.loads(body)
    a = data.get("node_a")
    b = data.get("node_b")

    repo.block_edge(a, b)
    return '{"message":"Edge blocked"}', 200

def handle_block_node(body):
    data = json.loads(body)
    node = data.get("node")

    repo.block_node(node)
    return '{"message":"Node blocked"}', 200
