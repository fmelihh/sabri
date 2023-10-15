import os
import pymongo
import fastapi


def execute_backend_server_event_handler(backend_app: fastapi.FastAPI):
    def launch_backend_server_events():
        backend_app.mongodb_client = pymongo.MongoClient(os.environ["MONGODB_URL"])

    return launch_backend_server_events
