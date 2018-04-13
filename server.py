from http.server import BaseHTTPRequestHandler, HTTPServer

presence_filename= "./blueping.txt"


class ServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        request_path = self.path

        if "key" in request_path:
            try:
                with open(presence_filename, "r") as file:
                    msg = file.read()
                    # print(msg)
                    self.wfile.write(bytes(msg, "ascii"))
            except FileNotFoundError:
                pass

        return


def run(ip, port):
    print('Starting server...')

    # For port 80 you need root access
    server_address = (ip, port)
    httpd = HTTPServer(server_address, ServerRequestHandler)
    print('Running server ', server_address)
    httpd.serve_forever()


run('0.0.0.0', 8066)
