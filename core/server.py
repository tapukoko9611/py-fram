import socket
from datetime import datetime
# from core.request import Request
# from core.response import Response
from request import Request
from response import Response

HOST = "0.0.0.0"
PORT = 8000
BUFF_SIZE = 16_384

def handle_client1(conn, addr):
    data = conn.recv(BUFF_SIZE)
    print("Data: ", data)
    print("Addr: ", addr)
    print(f"[{datetime.now():%H:%M:%S}] {addr} → {data.split(b' ')[0:2]}")
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: 13\r\n"
        b"Connection: close\r\n"
        b"\r\n"
        b"Hello, world"
    )
    conn.sendall(response)
    conn.close()

def handle_client(conn, addr):
    raw = conn.recv(BUFF_SIZE)
    req = Request(raw)
    if req.path == "/":
        res = Response(b"root!\n")
    elif req.path == "/hello":
        name = req.query.get("name", "anonymous").encode()
        res = Response(b"hello " + name + b"\n")
    else:
        res = Response(b"not found\n", "404 Not Found")
    conn.sendall(res.to_bytes())
    conn.close()

def serve_forever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    serve_forever()
