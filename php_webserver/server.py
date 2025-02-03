from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os

class PHPCGIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle PHP files
        if self.path.endswith('.php'):
            self.handle_php
        # Handle other files (HTML, CSS, JS)
        else:
            self.handle_static()
    def handle_php(self):
        script_path = self.get_script_path()

        if not os.path.exists(script_path):
            self.send_error(404, "File Not Found")
            return
        
        # prepare environment variables
        env = os.environ.copy()
        env['REQUEST_METHOD'] = 'GET'
        env['SCRIPT_FILENAME'] = script_path
        env['QUERY_STRING'] = self.path.split('?', 1)[1] if '?' in self.path else ''

        # Execute PHP-CGI
        try:
            result = subprocess.run(
                ['/usr/bin/php-cgi', script_path],
                env=env
                capture_output=True,
                text=True
            )
            # Split headers and content
            header_content = result.stdout.split('\r\n\r\n', 1)
            headers = header_content[0].split('\r\n')
            content = header_content[1] if len(header_content) > 1 else ''

            self.send_response(200)
            for header in headers:
                if ":" in header:
                    key, value = header.split(':', 1)
                    self.send_header(key.strip(), value.strip())
                self.end_headers()
                self.wfile.write(content.encode())
        except Exception as e:
            self.send_error(500, f"PHP Error: {str(e)}")

    def handle_static(self):
        file_path = self.get_script_path()

        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-Type', self.guess_mime_type(file_path))
            self.end_headers()
            self.wfile.write(content)
        except IOError:
            self.send_error(404, "File Not Found")
    
    def guess_mime_type(self, path):
        if path.endswith(".css"):
            return "text/css"
        if path.endswith(".js"):
            return "application/javascript"
        return "text/html"
    
def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PHPCGIRequestHandler)
    print(f"Server running on http://localhost:8000")
    httpd.server_forever()

if __name__ == '__main__':
    run_server()
