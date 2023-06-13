import os

from dotenv import load_dotenv
from supabase import create_client, Client

import schemas


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url=url, supabase_key=key)


def create_user(user: schemas.UserCreate):
    res = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password,
    })
    print(res.user)
    print("---")
    print(res.session)
