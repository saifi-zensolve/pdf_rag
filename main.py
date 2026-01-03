from dotenv import load_dotenv
from fastapi import FastAPI

from src.api import app_router, auth_router, ingest_router, llm_router

load_dotenv()

app = FastAPI()

app.include_router(llm_router)
app.include_router(auth_router)
app.include_router(app_router)
app.include_router(ingest_router)

if __name__ == "__main__":
    print("Run the app with: uvicorn main:app --reload")
    pass
