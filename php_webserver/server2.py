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

        })