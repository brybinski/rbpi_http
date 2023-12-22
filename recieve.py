#!/home/ryba/rbpi_qemu/python_project/venv/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
import jwt
import os


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_headers()
        secret = os.popen("cat ./secret").read().replace('\n', '')
        decode_test = jwt.decode(post_data, secret, algorithms="HS256")
        print(decode_test)


def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
