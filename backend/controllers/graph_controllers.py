import json
from repository import GraphRepository

repo = GraphRepository()

def handle_get_graph():
    return json.dumps(repo.get_graph())

def handle_post_node(body):
    data = json.loads(body)
    name = data.get("name")
    x = data.get("x", 0)
    y = data.get("y", 0)

    if not name:
        return '{"error":"Missing name"}', 400

    repo.create_node(name, x, y)
    return '{"message":"Node added"}', 201

def handle_post_edge(body):
    data = json.loads(body)
    a = data.get("a")
    b = data.get("b")
    w = data.get("weight")

    if not a or not b or w is None:
        return '{"error":"Missing parameters"}', 400

    repo.create_edge(a, b, w)
    return '{"message":"Edge added"}', 201

def handle_post_constraint(body):
    data = json.loads(body)
    a = data.get("a")
    b = data.get("b")
    penalty = data.get("penalty")

    repo.update_constraint(a, b, penalty)
    return '{"message":"Constraint updated"}', 200

def handle_block_edge(body):
    data = json.loads(body)
    a = data.get("a")
    b = data.get("b")

    repo.block_edge(a, b)
    return '{"message":"Edge blocked"}', 200

def handle_block_node(body):
    data = json.loads(body)
    node = data.get("node")

    repo.block_node(node)
    return '{"message":"Node blocked"}', 200
