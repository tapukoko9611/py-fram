from urllib.parse import urlparse, parse_qs

class Request:
    def __init__(self, raw: bytes):
        head, _, body = raw.partition(b"\r\n\r\n")
        lines = head.split(b"\r\n")
        req_line = lines[0].decode()
        self.method, self.target, self.version = req_line.split(" ")
        # Parse path + query
        parsed = urlparse(self.target)
        self.path = parsed.path
        self.query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        # Headers
        self.headers = {}
        for ln in lines[1:]:
            k, v = ln.decode().split(":", 1)
            self.headers[k.strip().lower()] = v.strip()
        self.body = body
