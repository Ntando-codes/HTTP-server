import http.server
import socketserver
import threading
import json
import logging

PORT = 7000

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"GET from {self.client_address[0]} to {self.path}")
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Welcome to Ntando's Server 🚀".encode())
        elif self.path == "/api/info":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = {"status": "running", "developer": "Ntando"}
            self.wfile.write(json.dumps(data).encode())
        elif self.path == "/shutdown":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Shutting down...")
            threading.Thread(target=httpd.shutdown).start()
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        logging.info(f"POST from {self.client_address[0]}")
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length)
        logging.info(f"Data received: {post_data.decode()}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST received!")

# Use a threaded server
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

httpd = ThreadedTCPServer(("", PORT), MyHandler)

server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()

print(f"✅ Ntando's advanced server is running at http://localhost:{PORT}")
input("Press Enter to stop server...\n")

httpd.shutdown()
httpd.server_close()
print("❌ Server stopped.")
# Ensure the server is properly closed