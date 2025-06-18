import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import jwt
from jwt import PyJWTError
from pathlib import Path

# Load secret key from environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")  # Empty string if not set
ALGORITHM = "HS256"

# Load CORS origins from environment variable
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")  # Default to "*" if not set

# Load CORS origins from environment variable
DATA_PATH = os.getenv("DATA_PATH", "/data")  # Default to "*" if not set

# FastAPI app
app = FastAPI()

# Configure CORS middleware for all origins or specific ones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if CORS_ORIGINS == "*" else CORS_ORIGINS.split(","),
    allow_methods=["GET"],  # Allowed HTTP methods
    #allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed HTTP methods
    allow_headers=["Authorization", "Content-Type"],  # Allowed headers
)

# Base directory for file storage (restrict access to this directory)
BASE_DIR = Path(DATA_PATH).resolve()
os.makedirs(BASE_DIR, exist_ok=True)

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to decode and validate JWT
def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency to validate JWT
def require_valid_jwt(token: str = Depends(oauth2_scheme)):
    if not SECRET_KEY:  # If SECRET_KEY is empty, skip JWT validation
        return
    decode_jwt(token)

# Endpoint: Serve files directly (no streaming)
@app.get("/file/{file_path:path}")
async def serve_file(file_path: str):
    # Resolve the full path and validate it
    full_path = (BASE_DIR / file_path).resolve()

    # Ensure the requested file is within the allowed directory
    if not full_path.is_file() or not str(full_path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=404, detail="File not found or unauthorized access")

    # Return the file directly (no streaming)
    return FileResponse(full_path)

# Function to stream file content
def stream_file(file_path: Path, chunk_size: int = 1024 * 1024):
    """Generator function to stream file content in chunks."""
    with open(file_path, "rb") as file:
        while chunk := file.read(chunk_size):  # Read file in chunks
            yield chunk

# Endpoint: Stream a file
@app.get("/stream/{file_path:path}")
async def stream_file_endpoint(file_path: str, token: str = Depends(require_valid_jwt)):
    # Resolve the full path
    full_path = (BASE_DIR / file_path).resolve()

    # Ensure the requested file is within the allowed directory
    if not full_path.is_file() or not str(full_path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=404, detail="File not found or unauthorized access")

    return StreamingResponse(stream_file(full_path), media_type="application/octet-stream")
