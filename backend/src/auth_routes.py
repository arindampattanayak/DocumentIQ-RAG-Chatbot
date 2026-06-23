from datetime import timedelta
import logging

from fastapi import APIRouter, HTTPException, status, Depends
from pymongo.errors import DuplicateKeyError

from src.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.db_utils import create_user, get_user_by_email
from src.dependencies import get_current_user
from src.pydantic_models import UserCreate, UserLogin, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(payload: UserCreate):
    try:
        existing_user = get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        password_hash = hash_password(payload.password)
        user_id = create_user(payload.name, payload.email, password_hash)

        token = create_access_token(
            data={
                "sub": user_id,
                "email": payload.email,
                "name": payload.name,
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return TokenResponse(
            access_token=token,
            user=UserOut(
                id=user_id,
                name=payload.name,
                email=payload.email,
            ),
        )

    except HTTPException:
        raise

    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    except Exception as e:
        logging.exception(f"Signup failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}",
        )


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    try:
        user = get_user_by_email(payload.email)
        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        token = create_access_token(
            data={"sub": user["id"], "email": user["email"], "name": user["name"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return TokenResponse(
            access_token=token,
            user=UserOut(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                created_at=user.get("created_at"),
            ),
        )

    except HTTPException:
        raise

    except Exception as e:
        logging.exception(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}",
        )


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return UserOut(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user.get("created_at"),
    )


@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    return {"message": "Logged out successfully."}