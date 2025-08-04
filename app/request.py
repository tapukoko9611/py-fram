import json
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs

class Request:
    def __init__(self, raw_data: bytes):
        self.raw = raw_data
        self.headers = {}
        self.body = b""
        self.path_params = {}

        head, _, body = raw_data.partition(b"\r\n\r\n")
        self.body = body
        lines = head.split(b"\r\n")

        # GET /path?query=1 HTTP/1.1
        method, target, version = lines[0].decode().split(" ")
        self.method = method
        self.target = target
        self.version = version

        parsed_url = urlparse(target)
        self.path = parsed_url.path
        self.query = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

        # Headers
        for line in lines[1:]:
            if b":" in line:
                k, v = line.decode().split(":", 1)
                self.headers[k.strip().lower()] = v.strip()

        # Parse cookies
        cookie_header = self.headers.get("cookie", "")
        self.cookies = {}
        if cookie_header:
            cookie = SimpleCookie()
            cookie.load(cookie_header)
            self.cookies = {k: v.value for k, v in cookie.items()}

    def json(self):
        try:
            return json.loads(self.body.decode())
        except:
            return {}

    def form(self):
        try:
            return {k: v[0] for k, v in parse_qs(self.body.decode()).items()}
        except:
            return {}

    def header(self, key: str) -> str:
        return self.headers.get(key.lower(), "")