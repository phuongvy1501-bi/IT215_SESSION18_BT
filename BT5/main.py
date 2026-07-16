from fastapi import FastAPI
from core.database import engine, Base
from api import students, workshops, registrations

# Tạo bảng (dùng cho dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống đăng ký Workshop")

app.include_router(students.router)
app.include_router(workshops.router)
app.include_router(registrations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Workshop Registration System"}
