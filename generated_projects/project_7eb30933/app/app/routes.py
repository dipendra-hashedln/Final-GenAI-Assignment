from fastapi import APIRouter
from app.security import BasicAuth
from app.models import User

router = APIRouter()

@router.post("/login")
async def login(user: User):
    auth = BasicAuth()
    credentials = await auth.authenticate(Request(), user)
    if credentials:
        return JSONResponse(content={"message": "Logged in successfully"}, media_type="application/json")
    return JSONResponse(content={"message": "Invalid credentials"}, media_type="application/json")
