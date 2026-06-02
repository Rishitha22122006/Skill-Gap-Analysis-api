from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Static Files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# -----------------------------
# Templates
# -----------------------------

templates = Jinja2Templates(
    directory="templates"
)

# -----------------------------
# Temporary User Storage
# -----------------------------

users = []

# -----------------------------
# Models
# -----------------------------

class RegisterData(BaseModel):
    username: str
    email: str
    password: str


class LoginData(BaseModel):
    email: str
    password: str


class SkillData(BaseModel):
    skills: str
    role: str


# -----------------------------
# HTML Pages
# -----------------------------

@app.get("/")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@app.get("/login-page")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/skills-page")
def skills_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="skills.html"
    )


# -----------------------------
# Register API
# -----------------------------

@app.post("/register")
def register(user: RegisterData):

    for existing_user in users:

        if existing_user["email"] == user.email:
            return {
                "message": "Email already exists"
            }

    users.append({
        "username": user.username,
        "email": user.email,
        "password": user.password
    })

    return {
        "message": "Registration Successful"
    }


# -----------------------------
# Login API
# -----------------------------

@app.post("/login")
def login(data: LoginData):

    for user in users:

        if (
            user["email"] == data.email
            and user["password"] == data.password
        ):
            return {
                "message": "Login Successful"
            }

    return {
        "message": "Invalid Email or Password"
    }


# -----------------------------
# Skill Analysis API
# -----------------------------

@app.post("/analyze")
def analyze(skill_data: SkillData):

    role_skills = {

        "frontend developer": [
            "html",
            "css",
            "javascript",
            "react"
        ],

        "backend developer": [
            "python",
            "fastapi",
            "api",
            "mysql"
        ],

        "data scientist": [
            "python",
            "machine learning",
            "numpy",
            "pandas"
        ]
    }

    role = skill_data.role.lower()

    user_skills = [
        skill.strip().lower()
        for skill in skill_data.skills.split(",")
    ]

    if role not in role_skills:
        return {
            "message": "Role not found"
        }

    required_skills = role_skills[role]

    missing_skills = []

    for skill in required_skills:
        if skill not in user_skills:
            missing_skills.append(skill)

    if len(missing_skills) == 0:
        return {
            "status": "Eligible",
            "message": f"You can pursue {role}",
            "missing_skills": []
        }

    return {
        "status": "Not Eligible",
        "message": f"You need more skills for {role}",
        "missing_skills": missing_skills
    }