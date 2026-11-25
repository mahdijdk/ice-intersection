import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sensors = {}

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/data":
            now = time.time()
            result = {}
            for sensor_id in sensors:
                item = dict(sensors[sensor_id])
                item["age"] = int(now - item["received"])
                result[sensor_id] = item
            body = json.dumps(result).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        else:
            file = open("index.html", "rb")
            body = file.read()
            file.close()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self):
        if self.path == "/data":
            length = int(self.headers["Content-Length"])
            text = self.rfile.read(length).decode("utf-8")
            data = json.loads(text)
            data["received"] = time.time()
            sensors[data["id"]] = data
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

port = int(os.environ.get("PORT", 8000))
server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
print("Server started on port", port)
server.serve_forever()
