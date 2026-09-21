"""Servidor temporário para publicar foto e áudio do render HeyGen."""
import http.server

DIRECTORY = "/data/work/heygen_public"
PORT = 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def guess_type(self, path):
        if str(path).endswith(".m4a"):
            return "audio/x-m4a"
        return super().guess_type(path)

    def log_message(self, *args):
        pass


with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
    httpd.serve_forever()
