# -*- coding: utf-8 -*-
import os
import json
import psycopg2
from math import hypot
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv  

# ------------------------------
# Chargement du .env
# ------------------------------
load_dotenv()

# ------------------------------
# Configuration de la base (depuis le .env)
# ------------------------------
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Connexion globale à la base
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ------------------------------
# Fonctions utilitaires SQL
# ------------------------------
def get_graph():
    """Récupère tous les nœuds et arêtes depuis la base."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, x, y, capacity FROM nodes;")
    nodes = {n[0]: {"id": n[0], "x": n[1], "y": n[2], "capacity": n[3]} for n in cur.fetchall()}

    cur.execute("SELECT u, v, weight FROM edges;")
    edges = [{"u": e[0], "v": e[1], "weight": e[2]} for e in cur.fetchall()]

    conn.close()
    return {"nodes": nodes, "edges": edges}


def add_node(node):
    """Ajoute un nœud dans la base PostgreSQL."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO nodes (id, x, y, capacity) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
        (node["id"], node["x"], node["y"], node["capacity"])
    )
    conn.commit()
    conn.close()


def add_edge(edge):
    """Ajoute une arête dans la base PostgreSQL."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO edges (u, v, weight) VALUES (%s, %s, %s);", (edge["u"], edge["v"], edge["weight"]))
    conn.commit()
    conn.close()


# ------------------------------
# Algorithmes de graphe
# ------------------------------
def build_adjacency(graph):
    """Crée une liste d’adjacence à partir des données SQL."""
    adj = {}
    for e in graph["edges"]:
        adj.setdefault(e["u"], []).append((e["v"], e["weight"]))
        adj.setdefault(e["v"], []).append((e["u"], e["weight"]))
    return adj


def dijkstra(graph, src, dst):
    """Algorithme de Dijkstra basique."""
    adj = build_adjacency(graph)
    dist = {n: float("inf") for n in graph["nodes"]}
    dist[src] = 0
    prev = {}
    q = [(0, src)]
    visited = set()

    while q:
        q.sort(reverse=True)
        d, u = q.pop()
        if u in visited:
            continue
        visited.add(u)
        if u == dst:
            break

        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                q.append((nd, v))

    # reconstruction du chemin
    path = []
    u = dst
    while u in prev:
        path.insert(0, u)
        u = prev[u]
    path.insert(0, src)
    return {"path": path, "distance": dist[dst]}


def greedy_coloring(graph):
    """Coloriage glouton simple (chaque couleur = jour/équipe)."""
    adj = build_adjacency(graph)
    colors = {}
    for node in graph["nodes"]:
        used = {colors[n] for n, _ in adj.get(node, []) if n in colors}
        color = 1
        while color in used:
            color += 1
        colors[node] = color
    return colors


# ------------------------------
# Serveur HTTP (API REST)
# ------------------------------
class RequestHandler(BaseHTTPRequestHandler):
    def _send_headers(self):
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        self.send_response(200)
        self._send_headers()

        if parsed.path == "/graph":
            self.wfile.write(json.dumps(get_graph()).encode())

        elif parsed.path == "/algo/dijkstra":
            graph = get_graph()
            src = query.get("src", [""])[0]
            dst = query.get("dst", [""])[0]
            res = dijkstra(graph, src, dst)
            self.wfile.write(json.dumps(res).encode())

        elif parsed.path == "/algo/coloring":
            graph = get_graph()
            res = greedy_coloring(graph)
            self.wfile.write(json.dumps(res).encode())

        else:
            self.wfile.write(json.dumps({"error": "endpoint inconnu"}).encode())

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length).decode())
        self.send_response(200)
        self._send_headers()

        if parsed.path == "/graph/node":
            add_node(body)
            self.wfile.write(json.dumps({"ok": True, "node": body}).encode())

        elif parsed.path == "/graph/edge":
            u, v = body["u"], body["v"]
            # Si aucun poids n’est fourni → calculer distance euclidienne
            if "weight" not in body:
                graph = get_graph()
                a, b = graph["nodes"][u], graph["nodes"][v]
                body["weight"] = hypot(a["x"] - b["x"], a["y"] - b["y"])
            add_edge(body)
            self.wfile.write(json.dumps({"ok": True, "edge": body}).encode())

        else:
            self.wfile.write(json.dumps({"error": "endpoint inconnu"}).encode())


# ------------------------------
# Lancement du serveur
# ------------------------------
if __name__ == "__main__":
    print("🚀 Serveur WasteGraph (PostgreSQL) lancé sur http://localhost:8080")
    HTTPServer(("localhost", 8080), RequestHandler).serve_forever()