from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.requests import Request

class BasicAuth:
    def __init__(self):
        self.users = {"user": "password"}

    async def authenticate(self, request: Request, credentials: HTTPBasicCredentials):
        if credentials.username in self.users and self.users[credentials.username] == credentials.password:
            return {"username": credentials.username}
        return None
