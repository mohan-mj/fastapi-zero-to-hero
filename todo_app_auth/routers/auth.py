from fastapi import APIRouter

from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext

router = APIRouter()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=50)
    role: str = Field(min_length=3, max_length=50)

@router.post('/auth/') 
def create_user(create_user: CreateUser):
    create_user_model = Users(
        username = create_user.username,
        password = bcrypt_context.hash(create_user.password),
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        email = create_user.email,
        role = create_user.role,
        is_active = True
    )
    return create_user_model