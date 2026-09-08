from datetime import datetime, timezone
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db, get_current_user
from backend.app.core.security import get_password_hash, verify_password, create_access_token
from backend.app.models.user import User
from backend.app.models.candidate import CandidateProfile
from backend.app.models.job import RecruiterProfile
from backend.app.schemas.auth import UserRegister, UserLogin, Token, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_role = data.role.upper()
    if user_role not in {"CANDIDATE", "RECRUITER"}:
        user_role = "CANDIDATE"

    user = User(
        email=data.email.lower(),
        hashed_password=get_password_hash(data.password),
        role=user_role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if user_role == "CANDIDATE":
        cand_id = f"CAND_{uuid.uuid4().hex[:7].upper()}"
        profile = CandidateProfile(
            user_id=user.id,
            candidate_id=cand_id,
            full_name=data.full_name or "Candidate",
            headline="Software Engineer",
            years_of_experience=2.0
        )
        db.add(profile)
    else:
        profile = RecruiterProfile(
            user_id=user.id,
            company_name=data.company_name or "HireSense Recruiting",
            industry="Technology"
        )
        db.add(profile)
    db.commit()

    token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        email=user.email
    )

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User account is deactivated")

    token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        email=user.email
    )

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
