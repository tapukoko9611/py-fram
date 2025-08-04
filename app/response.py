import json

class Response:
    def __init__(self, body: bytes, status: str = "200 OK", headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def to_bytes(self) -> bytes:
        headers = {
            "Content-Length": str(len(self.body)),
            "Connection": "close",
            "Content-Type": self.headers.get("Content-Type", "text/plain"),
            **self.headers,
        }
        head = "\r\n".join([f"HTTP/1.1 {self.status}"] + [f"{k}: {v}" for k, v in headers.items()])
        return head.encode() + b"\r\n\r\n" + self.body

    @classmethod
    def json(cls, obj: dict, status: str = "200 OK", headers=None):
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        body = json.dumps(obj).encode()
        return cls(body, status, headers)

    @classmethod
    def text(cls, text: str, status: str = "200 OK", headers=None):
        return cls(text.encode(), status, headers)

    def set_cookie(self, key, value, path="/", http_only=True):
        cookie = f"{key}={value}; Path={path}"
        if http_only:
            cookie += "; HttpOnly"
        self.headers["Set-Cookie"] = cookie
