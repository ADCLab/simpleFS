# simpleFS: A simple FastAPI-based File Server with JWT Authentication and CORS Support

simpleFS serves files directly and provides file streaming capabilities with optional JWT-based authentication and configurable Cross-Origin Resource Sharing (CORS). It is designed to restrict file access to a specified directory (`/data`) and supports secure API interactions.  By design simpleFS only allows for get operations.

## Features

- **File Serving**: Serve files directly from a restricted directory.
- **File Streaming**: Stream file content in chunks for efficient data transfer.
- **JWT Authentication**: Secure endpoints with token-based authentication.
- **CORS Support**: Configurable CORS origins for cross-domain API access.

## Folder Structure

```
project/
├── main.py               # FastAPI application code
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Docker Deployment
The simplist deployment is using docker.  An example docker-compose file is below. There are three confgurable environmental variables:
- JWT_SECRET_KEY
- CORS_ORIGINS

```
version: "3.9"

services:
  simplefs:
    image: adclab/simplefs:latest
    container_name: simplefs_app
    restart: always
    ports:
      - "8000:8000"  # Expose the application on port 8000
    environment:
      - JWT_SECRET_KEY=your_secret_key  # Replace with your actual secret key
      - CORS_ORIGINS=http://example.com,http://anotherwebsite.com  # Replace with allowed origins
    volumes:
      - ./data:/data  # Bind the host's ./data directory to the container's /data directory

```
## Endpoints

### 1. **Serve Files** (`GET /file/{file_path}`)
Serves files directly from the `/data` directory.

- **Request**:
  ```bash
  curl -X GET http://localhost:8000/file/example.txt
  ```

- **Response**:
  - Status `200`: Returns the requested file.
  - Status `404`: File not found or unauthorized access.

---

### 2. **Stream Files** (`GET /stream/{file_path}`)
Streams file content from the `/data` directory in chunks.

- **Request**:
  ```bash
  curl -X GET http://localhost:8000/stream/example.txt -H "Authorization: Bearer <JWT>"
  ```

- **Response**:
  - Status `200`: Streams the file content.
  - Status `401`: JWT is missing, expired, or invalid.
  - Status `404`: File not found or unauthorized access.

---

## JWT Authentication
simpleFS can function with or without a JWT.  Assumes you have a seperate JWT server to provide keys.  Validating JWT keys requires providing `JWT_SECRET_KEY`.  If the secret key is not provided then simpleFS will not validate. 

### Validating a JWT
The `/stream` endpoint requires a valid JWT for authorization unless `JWT_SECRET_KEY` is left empty (disables JWT validation).

## Configurable CORS

Control CORS behavior by setting the `CORS_ORIGINS` environment variable:
- Example:
  ```
  CORS_ORIGINS="http://example.com,http://anotherwebsite.com"
  ```
Set to `"*"` for development to allow requests from all origins.

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Deployment

For production, use a robust ASGI server like Gunicorn behind a reverse proxy (e.g., Nginx). Example:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

### Author

Adan Ernesto Vela
Associate Prof
Industrial Engineering &
Management Systems
Univ. of Central Florida
