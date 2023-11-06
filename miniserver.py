#!/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import argparse

# Accept some arguments
parser = argparse.ArgumentParser()
parser.add_argument('-sf', '--servefiles', action='store_true', required=False, default=False, help="Serve files in the directory miniserver runs in - Defaults to False")
parser.add_argument('-dp', '--disablepost', action='store_true', required=False, default=False, help="Disable server accepting POST requests")
parser.add_argument('-p', '--port', type=int, required=False, help="Port to listen on - Defaults to 8000")
args = parser.parse_args()

# Define ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Set bind port
bind_port = 8000

if args.port:
    bind_port = args.port


# Determine the behavior of the root path
serve_files = args.servefiles

if args.servefiles == True:
    print("Serving files from this directory")

# Create the "data" and "log" folders if they don't exist
if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('log'):
    os.makedirs('log')


def log_and_print(message, color=GREEN):
    tag = GREEN + "[LOG] " + RESET
    # Log the message to a file
    with open('log/server.log', 'a') as log_file:
        log_file.write(tag + message + '\n')
    # Print the message to the console with the specified color
    print(tag + message)

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global serve_files  # Access the global flag
        requested_page = self.path.lstrip('/')

        if self.path == '/':
            if serve_files:
                # List files in the directory
                file_list = os.listdir('.')
                html_response = '<html><body><h2>Miniserver:</h2><ul>'
                for file in file_list:
                    html_response += f'<li><a href="{file}">{file}</a></li>'
                html_response += '</ul></body></html>'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_response.encode('utf-8'))
                log_and_print(f"GET request received for {self.path} - Directory listing served.")
                return  # Place the return statement inside the if block

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'This is a GET request.')
            log_and_print(f"GET request received from {self.client_address[0]} for {self.path}")
        else:
            # Check if the requested page exists
            if os.path.exists(requested_page):
                if os.path.isdir(requested_page):
                    # Handle directory listing
                    file_list = os.listdir(requested_page)
                    directory = self.path  # Use self.path as the directory
                    html_response = (f"<html><body><h2>Miniserver - Directory Listing For {directory}:</h2><ul>")
                    for file in file_list:
                        html_response += f'<li><a href="{os.path.join(directory, file)}">{file}</a></li>'
                    html_response += '</ul></body></html>'
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_response.encode('utf-8'))
                    log_and_print(f"GET request received for {self.path} - Directory listing served.")
                else:
                    # Page exists, send the content
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open(requested_page, 'rb') as file:
                        self.wfile.write(file.read())
                    log_and_print(f"GET request received for {self.path} - Page served.")
            else:
                # Page does not exist, return a 404 Not Found response
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 Not Found: Page does not exist.')
                error_message = f"GET request received for {self.path} - 404 Not Found."
                log_and_print(RED + "[ERROR] " + RESET + error_message)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        client_ip = self.client_address[0]

        if args.disablepost:
            # Respond with a 405 Method Not Allowed status
            self.send_response(405)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'405 Method Not Allowed: POST requests are disabled.')
            log_and_print(RED + "[ERROR] " + RESET + "POST request received, but POST requests are disabled.")
        
            # Create a filename based on the client's IP address and timestamp
        else:
            timestamp = time.strftime("%d-%m-%Y@%H:%M:%S")
            filename = f"data/{client_ip}_{timestamp}.txt"

            title = "POST request from:" + client_ip + "@" + timestamp
            with open(filename, 'w') as file:
                file.write('POST from: ')
                file.write(client_ip)
                file.write(os.linesep)
                file.write('Time: ')
                file.write(timestamp)
                file.write(os.linesep)
                file.write('Post Data: ')
                file.write(os.linesep)
                file.write(post_data)
                file.write(os.linesep)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"200-OK".encode("utf-8"))
            log_and_print(f"POST request received from {client_ip} and saved to file: {filename}")

def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=bind_port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    log_and_print(f'Starting the server on port {port}. Press Ctrl+C to stop.')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log_and_print('Server stopped.')

if __name__ == '__main__':
    run()
