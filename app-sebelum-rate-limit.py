from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from html import escape

class LabHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
