import logging
from fastapi import FastAPI
from app.routes import document_routes, health_routes, query_routes  

# Configure logging to see error details in the console
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(document_routes.router)
app.include_router(health_routes.router)
app.include_router(query_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Document Management API"}
