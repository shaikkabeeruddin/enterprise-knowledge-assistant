from fastapi import FastAPI
from app.routes import upload
from app.routes import query

app = FastAPI()

app.include_router(upload.router, prefix="/upload")
app.include_router(query.router)

@app.get("/")
def root():
    return {"message": "Server is running"}