from urllib.parse import urlparse, parse_qs
from controllers.algorithm_controller import (
    handle_coloring,
    handle_dijkstra
)
from controllers.graph_controllers import (
    handle_get_graph,
    handle_post_node,
    handle_post_edge,
    handle_post_constraint,
)

def route_request(method, path, body=""):
    parsed = urlparse(path)
    route = parsed.path
    query_string = parsed.query
    query = {k: v[0] for k, v in parse_qs(query_string).items()} if query_string else {}


    if method == "GET" and route == "/graph":
        return handle_get_graph(), 200

    if method == "POST" and route == "/graph/node":
        return handle_post_node(body)

    if method == "POST" and route == "/graph/edge":
        return handle_post_edge(body)

    if method == "POST" and route == "/graph/constraint":
        return handle_post_constraint(body)

    if method == "GET" and route == "/algo/dijkstra":
        return handle_dijkstra(query), 200
    
    if method == "GET" and route == "/algo/coloring":
        return handle_coloring(), 200

    return '{"error":"Not found"}', 404
