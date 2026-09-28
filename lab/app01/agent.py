import json
import psutil
from http.server import BaseHTTPRequestHandler, HTTPServer


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps(
            {
                "cpu": psutil.cpu_percent(interval=0.3),
                "mem": psutil.virtual_memory().percent,
                "disk": psutil.disk_usage("/").percent,
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 9100), H).serve_forever()
