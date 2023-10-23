import uvicorn
from dotenv import load_dotenv

from api.routes import *

load_dotenv()


if __name__ == "__main__":
    uvicorn.run(backend_app, host="0.0.0.0", port=8000)
