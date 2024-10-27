# TinyGallery Backend Deployment Guide

This guide provides instructions for deploying the TinyGallery Backend in both development and production environments.

## Prerequisites

Before deploying the TinyGallery Backend, ensure you have the following:

- Python 3.6 or higher
- pip (Python package manager)
- virtualenv
- Git

## Development Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/WeepingDogel/tinygallery-backend.git
cd tinygallery-backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the necessary configuration:

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./database/database.sqlite
```

### 5. Run the Development Server

```bash
./debug.sh
```

The backend should now be running at `http://localhost:8000`.

## Production Deployment

For production deployment, we'll use Docker for containerization and easier management.

### 1. Build the Docker Image

```bash
docker build -t tinygallery-backend:latest .
```

### 2. Run the Docker Container

```bash
docker run -d -p 8000:8000 -v "./admin_list.json:/app/admin_list.json" --name tinygallery-backend tinygallery-backend:latest
```

This command:
- Runs the container in detached mode (`-d`)
- Maps port 8000 of the container to port 8000 on the host (`-p 8000:8000`)
- Mounts the `admin_list.json` file into the container (`-v "./admin_list.json:/app/admin_list.json"`)
- Names the container `tinygallery-backend`

### 3. Configure Reverse Proxy (Optional)

For production use, it's recommended to set up a reverse proxy (like Nginx) to handle incoming requests and forward them to your FastAPI application.

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Set Up SSL/TLS (Recommended)

For secure communication, set up SSL/TLS using a service like Let's Encrypt.

## Updating the Application

To update the application:

1. Pull the latest changes from the repository
2. Rebuild the Docker image
3. Stop and remove the old container
4. Run a new container with the updated image

```bash
git pull origin main
docker build -t tinygallery-backend:latest .
docker stop tinygallery-backend
docker rm tinygallery-backend
docker run -d -p 8000:8000 -v "./admin_list.json:/app/admin_list.json" --name tinygallery-backend tinygallery-backend:latest
```

## Monitoring and Logging

For production deployments, consider setting up monitoring and logging solutions. Some options include:

- Using Docker's built-in logging capabilities
- Implementing application-level logging in FastAPI
- Using a monitoring solution like Prometheus and Grafana

## Backup and Recovery

Regularly backup your database and any user-generated content. For SQLite:

```bash
docker exec tinygallery-backend sqlite3 /app/database/database.sqlite ".backup '/app/backups/backup.sqlite'"
```

Ensure you have a process in place to securely store these backups off-site.

## Troubleshooting

If you encounter issues:

1. Check the application logs:
   ```bash
   docker logs tinygallery-backend
   ```
2. Verify that all required environment variables are set correctly
3. Ensure that the `admin_list.json` file is properly mounted and accessible within the container

For more detailed troubleshooting, refer to the FastAPI and Docker documentation.

