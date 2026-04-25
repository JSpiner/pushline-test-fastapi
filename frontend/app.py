import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

start = time.time()


def filtered_env():
    # Strip K8s noise so the test view stays readable.
    ignore = ("PATH", "HOME", "HOSTNAME", "PWD", "LANG", "LC_ALL", "PYTHONPATH",
              "TERM", "SHLVL", "PYTHON_VERSION", "PYTHON_PIP_VERSION", "PYTHON_SETUPTOOLS_VERSION",
              "PYTHON_SHA256", "PYTHON_GET_PIP_URL", "PYTHON_GET_PIP_SHA256",
              "KUBERNETES_PORT", "KUBERNETES_PORT_443_TCP", "KUBERNETES_PORT_443_TCP_ADDR",
              "KUBERNETES_PORT_443_TCP_PORT", "KUBERNETES_PORT_443_TCP_PROTO",
              "KUBERNETES_SERVICE_HOST", "KUBERNETES_SERVICE_PORT", "KUBERNETES_SERVICE_PORT_HTTPS",
              "_placeholder")
    return {k: v for k, v in sorted(os.environ.items())
            if k not in ignore and not k.startswith("_")}


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "service": "frontend",
            "uptime_seconds": round(time.time() - start, 1),
            "injected_env": filtered_env(),
        }, indent=2)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, *a):
        return


if __name__ == "__main__":
    print("frontend: listening on :3000", flush=True)
    HTTPServer(("0.0.0.0", 3000), H).serve_forever()
