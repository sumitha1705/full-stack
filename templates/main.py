from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Database connection setup
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='database',  # Change this to your actual database name
            user='postgres',
            password='Isumitha',  # Change this to your actual password
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("✅ Database connected successfully")
        break
    except Exception as error:
        print("❌ Database connection failed:", error)
        time.sleep(3)

# Template directory
templates = Jinja2Templates(directory="templates")


# -------------------------
# Route: Show Signup Page
# -------------------------
@app.get("/signup", response_class=HTMLResponse)
async def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# -------------------------
# Route: Handle Signup Submission
# -------------------------
@app.post("/signup")
async def handle_signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        # Insert user data into the users table
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        print("✅ User registered successfully")

        # Redirect to login page
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

    except Exception as e:
        print("❌ Error inserting user:", e)
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "Signup failed. Please try again."
        })
    


# -------------------------
# Route: Show Login Page
# -------------------------
@app.get("/login", response_class=HTMLResponse)
async def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
