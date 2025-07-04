from fastapi import FastAPI, Security
from .db import Base, engine
from .login import user_login_router, get_current_active_user
from .scrape_router import scrape_router

app = FastAPI()
app.include_router(user_login_router)
app.include_router(scrape_router, dependencies=[Security(get_current_active_user)])
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Please login to use API"}
