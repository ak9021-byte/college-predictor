import os
from fastapi import APIRouter, UploadFile, File, Depends
from dependencies import require_admin
from db.session import SessionLocal
from models.upload_log import UploadLog

router = APIRouter()

UPLOAD_DIR = "data/uploads"

@router.post("/admin/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(require_admin)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, file.filename)

    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    db = SessionLocal()
    log = UploadLog(
        filename=file.filename,
        uploaded_by=current_user.id,
        status="uploaded"
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    db.close()

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "log_id": log.id
    }

@router.get("/admin/uploads")
def list_uploads(current_user = Depends(require_admin)):
    db = SessionLocal()
    logs = db.query(UploadLog).order_by(UploadLog.uploaded_at.desc()).all()
    db.close()
    return [
        {
            "id": log.id,
            "filename": log.filename,
            "uploaded_by": log.uploaded_by,
            "uploaded_at": log.uploaded_at,
            "status": log.status,
            "row_count": log.row_count
        }
        for log in logs
    ]
