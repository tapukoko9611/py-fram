from app.request import Request
from app.response import Response
from datetime import datetime

def logging_middleware(req: Request, res: Response, next_fn):
    print(f"[{datetime.now()}] {req.method} {req.path}")
    return next_fn()

def cors_middleware(req: Request, res: Response, next_fn):
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    res.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return next_fn()
