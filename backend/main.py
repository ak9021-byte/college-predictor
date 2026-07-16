from fastapi import FastAPI
from sqlalchemy import text
from db.session import engine

app = FastAPI()

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database_connected": True}
    except Exception as e:
        return {"status": "error", "database_connected": False, "error": str(e)}