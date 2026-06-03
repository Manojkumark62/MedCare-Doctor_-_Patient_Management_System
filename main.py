from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from database import Base, engine
from routers.auth import router as auth_router
from routers.appointments import router as appointment_router
from routers.doctors import router as doctor_router
from routers.billing import router as billing_router
from routers.notification import router as notification_router
from routers.patients import router as patient_router
from routers.reports import router as report_router

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 50)
    print("MedCare Hospital Management System Started")
    print("Swagger Docs : http://127.0.0.1:8000/docs")
    print("Redoc Docs   : http://127.0.0.1:8000/redoc")
    print("=" * 50)
    yield
    print("MedCare Hospital Management System Stopped")

app = FastAPI(title="MedCare Hospital Management System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"success": False, "message": str(exc)})

@app.get("/", tags=["System"])
def home():
    return {
        "success": True,
        "message": "Welcome to MedCare Hospital Management API",
        "version": "1.0.0"}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "UP", "database": "CONNECTED"}

app.include_router(auth_router)
app.include_router(appointment_router)
app.include_router(doctor_router)
app.include_router(billing_router)
app.include_router(notification_router)
app.include_router(patient_router)
app.include_router(report_router)