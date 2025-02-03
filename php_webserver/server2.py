import os
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer

class PHPRequestHandler(SimpleHTTPRequestHandler):
    def handle_php(self, script_path):
        env = os.environ.copy()
        env.update({
            'REQUEST_METHOD': self.command,
            'SCRIPT_FILENAME': script_path,
            'QUERY_STRING': self.path.split('?', 1)[1] if '?' in self.path else '',
            'CONTENT_TYPE': self. headers.get('Content_Type', ''),
            'CONTENT_LENGTH': self.headers.get('Content-Length', ''),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': str(self.server.server_port),
            'GATEWAY_INTERFACE': 'CGI/1/1',
            'SERVER_PROTOCOL': self.request_version,
            'REQUEST_URI': self.path
        })

        input_data = None
        if self.command == 'POST':
            content_length = int(self.headers.get('Content_Length', 0))
            input_data = self.rfile.read(content_length)

        process = subprocess.Popen(
            ['php-cgi', script_path],
            env=env,
            stdin=subprocess.PIPE if input_data else None,
            stdout=subprocess.PIPEm
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=input_data)

        if process.returncode != 0:
            self.send_error(500, "PHP Execution Error")
            print("PHP Error:", stderr.decode())
            return None, None

        response = stdout.decode('utf-8'
        if '\r\n\r\n' in response:
            headers, body = '', response)
        return headers.split('\r\n'), body