import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from supabase import create_client, Client

import schemas
import trim
import fisheye
import sin
import mosaic


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


@router.post("/image", tags=['user'])
def transform_image(path: str):
    res = supabase.storage().from_("Images").download(path)
    p = path.replace("/", "")[6:-4]
    filepath = f"./tmp/{p}.png"
    with open(filepath, "wb+") as f:
        f.write(res)

    trim_path = trim.process_image(filepath, p)
    fisheye.processing_fish(trim_path, p)
    sin.processing_sin(trim_path, p)
    mosaic.processing_mosaic(trim_path, p)
