from fastapi import APIRouter
from . import models, tasks, views

users_router = APIRouter(
    prefix='/users'
)

