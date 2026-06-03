https://chatgpt.com/share/6a1deebf-30e4-8322-97b9-b3586c54b11f





For a production-ready FastAPI project, the folder structure is usually more than just models, schemas, core, utils, routers, and crud.

A clean scalable structure looks like this:

project/
│
├── app/
│   │
│   ├── main.py
│   ├── api/
│   │   ├── routers/
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   └── product.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── database.py
│   │   ├── settings.py
│   │   └── constants.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── crud/
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   └── payment_service.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── init_db.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── logger.py
│   │   └── file_handler.py
│   │
│   ├── middleware/
│   │   ├── auth.py
│   │   ├── logging.py
│   │   └── cors.py
│   │
│   ├── exceptions/
│   │   ├── handlers.py
│   │   └── custom_exceptions.py
│   │
│   ├── templates/
│   │
│   ├── static/
│   │
│   ├── background_tasks/
│   │   ├── celery_tasks.py
│   │   └── scheduler.py
│   │
│   ├── websocket/
│   │   └── notification.py
│   │
│   ├── permissions/
│   │   └── roles.py
│   │
│   └── tests/
│       ├── test_auth.py
│       └── test_user.py
│
├── alembic/
│
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
What Each Folder Does

1. main.py

Application entry point.

app = FastAPI()

Registers routers and middleware.

2. routers/

API endpoints.

Example:

POST /users
GET /users

Only handles request/response.

3. schemas/

Pydantic validation.

Example:

UserCreate
UserUpdate
UserResponse

Input/output validation.

4. models/

SQLAlchemy DB tables.

Example:

User
Product
Order

Actual database structure.

5. crud/

Database queries.

Example:

create_user()
get_user()
update_user()

Keeps DB logic separate.

6. services/ (Very Important)

Business logic.

Example:

JWT creation
OTP
Email sending
Payment logic

Router → Service → CRUD

This keeps code clean.

7. core/

Project configuration.

Usually:

settings
database
JWT
security
config

Example:

SECRET_KEY
DATABASE_URL
8. db/

Database connection setup.

Usually:

SessionLocal
Base
engine
9. utils/

Reusable helpers.

Examples:

date formatter
password generator
image resize
common functions
10. middleware/

Runs before request reaches router.

Examples:

logging
auth checks
request timing
CORS
11. exceptions/

Central error handling.

Example:

404
403
validation errors
custom exceptions
12. permissions/

Role-based access.

Example:

admin only
staff only
customer only
13. background_tasks/

Async jobs.

Examples:

email sending
report generation
scheduler
Celery
14. websocket/

Real-time features.

Examples:

notifications
chat
live updates
15. tests/

Pytest test cases.

Example:

test_auth.py
test_users.py
16. alembic/

Database migrations.

Example:

alembic revision
alembic upgrade head
Recommended Layer Flow
Router
   ↓
Service
   ↓
CRUD
   ↓
Model / DB

and

Request
   ↓
Schema Validation
   ↓
Router
   ↓
Response Schema

For your FastAPI + React production architecture, I would recommend:

api/
core/
db/
models/
schemas/
crud/
services/
utils/
middleware/
permissions/
tests/

This is close to real industry structure.

I will demonstrate the complete FastAPI flow using a simple User API.

The flow is:

Request
   ↓
Router
   ↓
Schema Validation
   ↓
Service (optional business logic)
   ↓
CRUD
   ↓
Model
   ↓
Database
   ↓
Response Schema

Project structure:

app/
│
├── main.py
├── core/
│   └── database.py
├── models/
│   └── user.py
├── schemas/
│   └── user.py
├── crud/
│   └── user.py
├── routers/
│   └── user.py
└── services/
    └── user_service.py
Step 1 — Database Connection
core/database.py

Create DB connection.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Step 2 — Model
models/user.py

DB table structure.

from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)

Model = Database table.

Step 3 — Schema
schemas/user.py

Request and response validation.

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True

Schemas handle:

Input:

POST data

Output:

API response
Step 4 — CRUD
crud/user.py

Only DB queries.

from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, data):
    user = User(
        name=data.name,
        email=data.email,
        phone=data.phone
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(
        User.id == user_id
    ).first()

CRUD = DB operations only.

No API logic.

Step 5 — Service Layer
services/user_service.py

Business logic.

Example:

duplicate email check
password hash
OTP
permissions
from fastapi import HTTPException
from app.crud.user import create_user
from app.models.user import User

def create_user_service(db, data):

    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return create_user(db, data)

Service = Business rules.

Step 6 — Router
routers/user.py

API endpoints.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import get_users, get_user
from app.services.user_service import create_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=UserResponse
)
def create(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user_service(db, data)

@router.get(
    "/",
    response_model=list[UserResponse]
)
def list_users(
    db: Session = Depends(get_db)
):
    return get_users(db)

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def detail(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user(db, user_id)

Router only handles:

endpoint
dependency
request
response
Step 7 — Main App
main.py

Register router.

from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.user import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

Run:

uvicorn app.main:app --reload
API Demonstration
1 Create User

POST

/users

Body:

{
  "name": "Jay",
  "email": "jay@gmail.com",
  "phone": "9999999999"
}

Flow:

Router
↓
Schema validates
↓
Service checks email
↓
CRUD inserts
↓
Model saves
↓
DB commit
↓
Response schema

Response:

{
  "id": 1,
  "name": "Jay",
  "email": "jay@gmail.com",
  "phone": "9999999999"
}
2 Get All Users

GET

/users

Response:

[
  {
    "id":1,
    "name":"Jay",
    "email":"jay@gmail.com",
    "phone":"9999999999"
  }
]
3 Get One User

GET

/users/1

Complete endpoint flow:

Client
 ↓
Router
 ↓
Schema
 ↓
Service
 ↓
CRUD
 ↓
Model
 ↓
Database
 ↓
Response

This is the basic architecture used in many real FastAPI projects.
