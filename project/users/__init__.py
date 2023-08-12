from fastapi import APIRouter
from . import models

users_router = APIRouter(
    prefix='users/'
)
