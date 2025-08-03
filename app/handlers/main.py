from app.response import Response

def index_handler(req):
    return Response(b"Hello, World!\n")

def hello_handler(req):
    name = req.query.get("name", "Anonymous").encode()
    return Response(b"Hello, " + name + b"\n")

def user_handler(req):
    user_id = req.path_params.get("id", "unknown").encode()
    return Response(b"User ID: " + user_id + b"\n")