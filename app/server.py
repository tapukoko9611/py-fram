import socket
from app.router import Router
from app.request import Request
from app.response import Response
from app.handlers import main

HOST = "0.0.0.0"
PORT = 8000
BUFF_SIZE = 16_384

ROUTES = {
    "/": main.index_handler,
    "/hello": main.hello_handler,
}
router = Router()
router.get("/")(main.index_handler)
router.get("/hello")(main.hello_handler)
router.get("/user/{id}")(main.user_handler)

def handle_client1(conn, addr):
    raw = conn.recv(BUFF_SIZE)
    if not raw:
        conn.close()
        return

    try:
        req = Request(raw)
        handler = ROUTES.get(req.path)

        if handler:
            res = handler(req)
        else:
            res = Response(b"404 Not Found\n", status="404 Not Found")

    except Exception as e:
        res = Response(f"500 Internal Server Error\n{str(e)}\n".encode(), status="500 Internal Server Error")

    conn.sendall(res.to_bytes())
    conn.close()

def handle_client(conn, addr):
    raw = conn.recv(16_384)
    if not raw:
        conn.close()
        return

    try:
        req = Request(raw)
        match = router.resolve(req.method, req.path)

        if match:
            handler, path_params = match
            req.path_params = path_params
            res = handler(req)
        else:
            res = Response(b"404 Not Found\n", "404 Not Found")
    except Exception as e:
        res = Response(f"500 Server Error\n{str(e)}".encode(), "500 Internal Server Error")

    conn.sendall(res.to_bytes())
    conn.close()

def serve_forever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT} ...")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    serve_forever()
