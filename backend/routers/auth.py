from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from db.session import SessionLocal
from models.user import User
from schemas.user import SignupRequest, UserResponse, LoginRequest, TokenResponse
from core.security import verify_password, create_access_token
from dependencies import get_current_user, require_admin

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/auth/signup", response_model=UserResponse)
def signup(request: SignupRequest):
    db = SessionLocal()

    existing_user = db.query(User).filter_by(email=request.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(request.password)
    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user

@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter_by(email=request.email).first()
    db.close()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.role)
    return TokenResponse(access_token=token, role=user.role)

@router.get("/auth/me")
def get_me(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}

@router.get("/auth/admin-only")
def admin_only_route(current_user = Depends(require_admin)):
    return {"message": f"Welcome admin {current_user.email}"}