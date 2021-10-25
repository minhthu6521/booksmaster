from starlette.requests import Request

from views.utils import app
import views


@app.get("/")
def read_root(request: Request):
    return {"documentation": f"{request.base_url.hostname}:{request.base_url.port}/docs"}
