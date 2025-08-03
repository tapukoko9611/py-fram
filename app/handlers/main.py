from app.response import Response

def index_handler(request):
    return Response(b"Hello, World!\n")

def hello_handler(request):
    name = request.query.get("name", "Anonymous").encode()
    return Response(b"Hello, " + name + b"\n")
