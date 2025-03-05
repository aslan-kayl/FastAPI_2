from fastapi import FastAPI

from src.admin_panel.answer.routes import answer_router
from src.admin_panel.banner.routes import banner_router
from fastapi.staticfiles import StaticFiles
from src.auth.routers import auth_router
from src.admin_panel.info.routes import info_router
from src.admin_panel.question.routes import question_router

version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Bookly",
    description=description,
    version=version,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(banner_router, prefix=f"/api/{version}/banner", tags=["banner"])
app.include_router(info_router, prefix=f"/api/{version}/info", tags=["info"])
app.include_router(question_router, prefix=f"/api/{version}/question", tags=["question"])
app.include_router(answer_router, prefix=f"/api/{version}/answer", tags=["answer"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
