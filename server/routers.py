import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from supabase import create_client, Client

import schemas
import crud


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=url, supabase_key=key)


router = APIRouter()


@router.post("/auth/signup", tags=['user'])
def signup(user: schemas.UserCreate):
    res = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password,
    })
    data, count = supabase.table('User').insert(
        {
            "email": res.user.email,
            "user_id": res.user.id,
            "user_name": "Unknown",
        }
    ).execute()
    return {"user_id": res.user.id, "email": res.user.email}


@router.post("/auth/signin", tags=['user'])
def signin(user: schemas.UserCreate):
    res = supabase.auth.sign_in_with_password({
        "email": user.email,
        "password": user.password
    })
    return {"user_id": res.user.id, "email": res.user.email}
