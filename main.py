import uvicorn
from dotenv import load_dotenv

from src.chat_app.api.app import backend_app

load_dotenv()


if __name__ == "__main__":
    uvicorn.run(backend_app, host="0.0.0.0", port=8000)
