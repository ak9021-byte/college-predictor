from fastapi import FastAPI
from sqlalchemy import text
from db.session import engine, SessionLocal
from models.cutoff import Cutoff
from routers.auth import router as auth_router
from routers.admin import router as admin_router
from routers.predict import router as predict_router


app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(predict_router, prefix="/api")

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database_connected": True}
    except Exception as e:
        return {"status": "error", "database_connected": False, "error": str(e)}



@app.get("/api/categories")
def get_categories():
    db = SessionLocal()
    categories = db.query(Cutoff.category).distinct().order_by(Cutoff.category).all()
    db.close()
    return {"categories": [c[0] for c in categories]}