from starlette.requests import Request

from app import app


@app.get("/")
def read_root(request: Request):
    return {"documentation": f"{request.base_url.hostname}:{request.base_url.port}/docs"}
