from fastapi import FastAPI
from core.database import engine, Base
from api.routes import router

# Tạo các bảng trong DB (dùng cho mục đích dev)
# Trong production nên dùng Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LMS API - Bài tập 4")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Baitap4 API"}
