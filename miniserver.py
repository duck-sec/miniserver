from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import time
import os

# Define ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Set a flag to determine the behavior of the root path
serve_files = False

def log_and_print(message, color=GREEN):
    tag = GREEN + "[LOG] " + RESET
    # Log the message to a file
    with open('server.log', 'a') as log_file:
        log_file.write(tag + message + '\n')
    
    # Print the message to the console with the specified color
    print(tag + message)

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global serve_files  # Access the global flag

        if self.path == '/':
            if serve_files:
                # List files in the directory
                file_list = os.listdir('.')
                html_response = '<html><body><h2>Files in the directory:</h2><ul>'
                for file in file_list:
                    html_response += f'<li><a href="{file}">{file}</a></li>'
                html_response += '</ul></body></html>'

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_response.encode('utf-8'))
                log_and_print(f"GET request received for {self.path} - File list served.")
                return  # Place the return statement inside the if block

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'This is a GET request.')
            log_and_print(f"GET request received from {self.client_address[0]} for {self.path}")
        else:
            # Check if the requested page exists
            requested_page = self.path.lstrip('/')
            if os.path.exists(requested_page):
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
        
        # Create a filename based on the client's IP address and timestamp
        timestamp = time.strftime("%d-%m-%Y@%H:%M:%S")
        filename = f"{client_ip}_{timestamp}.txt"

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
        self.wfile.write(f'[LOG] POST data saved to file: {filename}'.encode("utf-8"))
        log_and_print(f"POST request received from {client_ip} and saved to file: {filename}")

def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    log_and_print(f'Starting the server on port {port}. Press Ctrl+C to stop.')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log_and_print('Server stopped.')

if __name__ == '__main__':
    run()
