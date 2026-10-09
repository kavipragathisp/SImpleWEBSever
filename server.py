from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST = "localhost"
PORT = 8000
HTML_FILE = Path(__file__).parent / "welcome.html"


class WelcomeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html", "/welcome.html"):
            try:
                content = HTML_FILE.read_bytes()
            except FileNotFoundError:
                self.send_error(500, "welcome.html not found next to server.py")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "Page not found")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), WelcomeHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
