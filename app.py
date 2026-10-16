
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from html import escape
from collections import defaultdict, deque
from threading import Lock
from time import monotonic

WINDOW_SECONDS = 10
MAX_REQUESTS = 30

request_times = defaultdict(deque)
rate_lock = Lock()


class LabHandler(BaseHTTPRequestHandler):
    def is_rate_limited(self):
        client = self.client_address[0]
        now = monotonic()

        with rate_lock:
            history = request_times[client]

            while history and now - history[0] >= WINDOW_SECONDS:
                history.popleft()

            if len(history) >= MAX_REQUESTS:
                return True

            history.append(now)
            return False

    def do_GET(self):
        if self.is_rate_limited():
            body = b"Terlalu banyak request. Coba lagi nanti."
            self.send_response(429)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Retry-After", str(WINDOW_SECONDS))
            self.end_headers()
            self.wfile.write(body)
            return

        query = parse_qs(urlparse(self.path).query)
        pesan = query.get("q", [""])[0]

        if len(pesan) > 100:
            self.send_error(400, "Input maksimal 100 karakter")
            return

        halaman = f"""<!doctype html>
<html lang="id">
<head><meta charset="utf-8"><title>Web Security Lab</title></head>
<body>
<h1>Lab Pencarian</h1>
<form method="GET">
  <input name="q" placeholder="Masukkan kata pencarian">
  <button type="submit">Cari</button>
</form>
<p>Hasil pencarian: {escape(pesan)}</p>
</body>
</html>"""

        isi = halaman.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(isi)))
        self.end_headers()
        self.wfile.write(isi)


ThreadingHTTPServer(("127.0.0.1", 8081), LabHandler).serve_forever()
