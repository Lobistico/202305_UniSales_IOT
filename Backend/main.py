from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title='API - Tarefas')
app.include_router(api_router, prefix=settings.API_V1)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def main():
    return {"message": "Hello World"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=8080, log_level='info', reload=True)