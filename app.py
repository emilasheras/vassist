from fastapi import FastAPI
from controllers.api_controller import APIController
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Check for WS_APP_PORT and ensure it's valid
port = os.getenv("WS_APP_PORT")
if not port or not port.isdigit():
    raise ValueError("Error: Debe definir el valor de 'WS_APP_PORT' en el archivo .env y debe ser un número válido.")

app = FastAPI(openapi_url=f"/api/v1/openapi.json", docs_url=f"/api/v1/docs")
api_controller = APIController(app)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(port), reload=True)
