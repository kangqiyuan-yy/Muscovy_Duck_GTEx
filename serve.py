#!/usr/bin/env python3
"""
Static HTTP server with gzip pre-compressed file support.
Usage:  python3 serve.py [port]   (default: 8080)
"""
import sys
import os
import mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
ROOT = os.path.dirname(os.path.abspath(__file__))

COMPRESSIBLE = {'.json', '.js', '.css', '.html', '.tsv', '.txt'}


class GzipHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        path = self.translate_path(self.path)
        _, ext = os.path.splitext(path)
        gz_path = path + '.gz'
        accept_enc = self.headers.get('Accept-Encoding', '')

        if ('gzip' in accept_enc
                and ext in COMPRESSIBLE
                and os.path.isfile(gz_path)):
            ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
            size = os.path.getsize(gz_path)
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(size))
            self.send_header('Vary', 'Accept-Encoding')
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.end_headers()
            with open(gz_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

    def log_message(self, fmt, *args):
        # Only log non-200/304 responses
        if args and str(args[1]) not in ('200', '304'):
            super().log_message(fmt, *args)


os.chdir(ROOT)
httpd = ThreadingHTTPServer(('', PORT), GzipHandler)
httpd.daemon_threads = True
print('Muscovy Duck GTEx server: http://localhost:%d/' % PORT)
httpd.serve_forever()
