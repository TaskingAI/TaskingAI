import uvicorn
from app.config import CONFIG

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=CONFIG.SERVICE_PORT, reload=True)
