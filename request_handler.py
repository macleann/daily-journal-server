import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_entries, get_single_entry, get_queried_entries, create_entry, update_entry, delete_entry, get_all_moods, get_single_mood, create_mood, update_mood, delete_mood, get_all_tags, get_entrytags_by_id

class HandleRequests(BaseHTTPRequestHandler):
    """Main class for handling requests

    Args:
        BaseHTTPRequestHandler (class): Class from http.server
    """
    def do_GET(self):
        """Handles GET requests to the server"""
        response = {}

        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "entries":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_entry(id)
                else:
                    self._set_headers(200)
                    response = get_all_entries()
            elif resource == "moods":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_mood(id)
                else:
                    self._set_headers(200)
                    response = get_all_moods()
            elif resource == "tags":
                self._set_headers(200)
                response = get_all_tags()
            else:
                self._set_headers(400)
                response = []
        else:
            (resource, query) = parsed

            if resource == 'entries':
                if 'q' in query:
                    self._set_headers(200)
                    response = get_queried_entries(query['q'][0])
            elif resource == "entrytags":
                if 'entry_id' in query:
                    self._set_headers(200)
                    response = get_entrytags_by_id(query['entry_id'][0])

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_resource = None

        if resource == "entries":
            self._set_headers(201)
            new_resource = create_entry(post_body)
        elif resource == "moods":
            self._set_headers(201)
            new_resource = create_mood(post_body)
        else:
            self._set_headers(401)
            new_resource = 'Not a valid POST request'

        self.wfile.write(json.dumps(new_resource).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            success = update_entry(id, post_body)
        elif resource == "moods":
            success = update_mood(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handles DELETE requests to the server"""
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)
        elif resource == "moods":
            delete_mood(id)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
