class Response:
    def __init__(self, body: bytes, status: str = "200 OK", headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def to_bytes(self):
        h = {
            "Content-Length": str(len(self.body)),
            "Connection": "close",
            **self.headers,
        }
        head_lines = [f"HTTP/1.1 {self.status}"]
        head_lines += [f"{k}: {v}" for k, v in h.items()]
        head = "\r\n".join(head_lines).encode() + b"\r\n\r\n"
        return head + self.body
