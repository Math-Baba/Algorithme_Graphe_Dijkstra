from http.server import BaseHTTPRequestHandler, HTTPServer
from route import route_request
import json

class App(BaseHTTPRequestHandler):

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        response, code = route_request("GET", self.path)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._set_cors_headers()
        self.end_headers()
        # Si response est déjà une string, l'encoder directement, sinon le convertir en JSON
        if isinstance(response, str):
            self.wfile.write(response.encode())
        else:
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        response, code = route_request("POST", self.path, body)

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(response.encode())

    def do_DELETE(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length > 0 else ""
        response, code = route_request("DELETE", self.path, body)

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._set_cors_headers()
        self.end_headers()
        if isinstance(response, str):
            self.wfile.write(response.encode())
        else:
            self.wfile.write(json.dumps(response).encode())

def run():
    print("Backend running at http://localhost:5000")
    HTTPServer(("localhost", 5000), App).serve_forever()

if __name__ == "__main__":
    run()
