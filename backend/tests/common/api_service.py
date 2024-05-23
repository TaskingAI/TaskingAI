from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get(
    "/action_length",
)
def list_items(kb: int = 5):
    return "*"*1024*kb


if __name__ == "__main__":

    uvicorn.run("api_service:app", host="127.0.0.1", port=8001, reload=True)
