from fastapi import FastAPI
from sqlalchemy import text
from db.session import engine
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api")

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database_connected": True}
    except Exception as e:
        return {"status": "error", "database_connected": False, "error": str(e)}