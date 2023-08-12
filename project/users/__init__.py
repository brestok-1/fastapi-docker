from fastapi import APIRouter
from . import models, tasks

users_router = APIRouter(
    prefix='users/'
)

