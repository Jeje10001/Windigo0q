import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import bot

def health():
    port = int(os.environ.get("PORT", 8080))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, *a):
            pass
    HTTPServer(("0.0.0.0", port), H).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=health, daemon=True).start()
    bot.main()
