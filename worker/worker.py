import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

start = time.time()
jobs_done = 0


def background_loop():
    global jobs_done
    while True:
        time.sleep(5)
        jobs_done += 1
        print(f"[worker] processed job #{jobs_done}", flush=True)


threading.Thread(target=background_loop, daemon=True).start()


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "service": "worker",
            "uptime_seconds": round(time.time() - start, 1),
            "jobs_done": jobs_done,
        }, indent=2)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, *a):
        return


if __name__ == "__main__":
    print("worker: listening on :9000, processing jobs every 5s", flush=True)
    HTTPServer(("0.0.0.0", 9000), H).serve_forever()
