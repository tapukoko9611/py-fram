from app.response import Response

def index_handler(req):
    return Response.text("Hello, World!")

def hello_handler(req):
    name = req.query.get("name", "Anonymous")
    return Response.text(f"Hello, {name}!")

def user_handler(req):
    user_id = req.path_params.get("id", "unknown")
    return Response.text(f"User ID: {user_id}")

def echo_json(req):
    if req.header("content-type") == "application/json":
        data = req.json()
    else:
        data = {"error": "Expected JSON"}
    return Response.json({"you_sent": data})
