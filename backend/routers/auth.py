from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from db.session import SessionLocal
from models.user import User
from schemas.user import SignupRequest, UserResponse, LoginRequest, TokenResponse
from core.security import verify_password, create_access_token

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