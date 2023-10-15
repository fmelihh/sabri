import fastapi
from config.events import execute_backend_server_event_handler


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.add_event_handler(
        "startup", execute_backend_server_event_handler(backend_app=app)
    )
    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

__all__ = ["backend_app"]
