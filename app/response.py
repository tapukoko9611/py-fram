class Response:
    def __init__(self, body: bytes, status: str = "200 OK", headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def to_bytes(self) -> bytes:
        headers = {
            "Content-Length": str(len(self.body)),
            "Content-Type": "text/plain",
            "Connection": "close",
            **self.headers,
        }
        lines = [f"HTTP/1.1 {self.status}"] + [f"{k}: {v}" for k, v in headers.items()]
        return ("\r\n".join(lines) + "\r\n\r\n").encode() + self.body
