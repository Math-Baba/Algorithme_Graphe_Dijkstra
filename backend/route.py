from urllib.parse import urlparse
from controllers.graph_controllers import (
    handle_get_graph,
    handle_post_node,
    handle_post_edge,
    handle_post_constraint,
    handle_block_edge,
    handle_block_node
)

def route_request(method, path, body=""):
    parsed = urlparse(path)
    route = parsed.path

    if method == "GET" and route == "/graph":
        return handle_get_graph(), 200

    if method == "POST" and route == "/graph/node":
        return handle_post_node(body)

    if method == "POST" and route == "/graph/edge":
        return handle_post_edge(body)

    if method == "POST" and route == "/graph/constraint":
        return handle_post_constraint(body)

    if method == "POST" and route == "/graph/block-edge":
        return handle_block_edge(body)

    if method == "POST" and route == "/graph/block-node":
        return handle_block_node(body)

    return '{"error":"Not found"}', 404
