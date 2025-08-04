from datetime import datetime
from app.request import Request
from app.response import Response
from app.auth import get_session

def logging_middleware(req: Request, res: Response, next_fn):
    print(f"[{datetime.now()}] {req.method} {req.path}")
    return next_fn()

def cors_middleware(req: Request, res: Response, next_fn):
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    res.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return next_fn()

def session_middleware(req, res, next_fn):
    token = req.cookies.get("session")
    req.user = None
    if token:
        session = get_session(token)
        if session:
            req.user = {"id": session["user_id"]}
    return next_fn()