from fastapi import FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel

app = FastAPI()
