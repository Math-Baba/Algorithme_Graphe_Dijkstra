# server.py

from http.server import BaseHTTPRequestHandler, HTTPServer
from route import route_request

class App(BaseHTTPRequestHandler):

    def do_GET(self):
        response, code = route_request("GET", self.path)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        response, code = route_request("POST", self.path, body)

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())

def run():
    print("Backend running at http://localhost:8000")
    HTTPServer(("localhost", 8000), App).serve_forever()

if __name__ == "__main__":
    run()
