from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os

class PHPCGIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle PHP files
        if self.path.endswith('.php'):
            self.handle_php
            