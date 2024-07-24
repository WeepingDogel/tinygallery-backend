# TinyGallery Backend (FastAPI)

## Introduction

The TinyGallery Backend is a RESTful API built using FastAPI that powers the TinyGallery Vue Edition. It provides basic CRUD functionality for managing images and categories.

## API Documentation

The API endpoints are documented using Swagger UI. Once the backend server is up and running, you can access the Swagger UI documentation by going to [http://localhost:8000/docs](http://localhost:8000/docs) in your web browser.

## Requirements

* Python 3.6 or higher
* pip
* virtualenv

## Getting Started

Follow these steps to get started with the TinyGallery Backend:

### Clone the repository:

```shell
git clone https://github.com/WeepingDogel/tinygallery-backend.git
```

### Change into the project directory:

```shell
cd tinygallery-backend
```

### Create a new virtual environment:

```shell
virtualenv venv
```

### Activate the virtual environment:

```shell
source venv/bin/activate
```

### Install the required dependencies:

```shell
pip install -r requirements.txt
```

### Start the backend server:

```shell
./debug.sh
```

Alternatively, if you want to run the server in a production environment:

```shell
./run.sh
```

The backend server should now be running at [http://localhost:8000](http://localhost:8000).

## Docker Deployment

To deploy the backend using Docker, follow these steps:

### Build the Docker image:

```shell
docker build -t your_registry_url/tinygallery-backend:latest .
```

### Push the Docker image to your registry:

```shell
docker push your_registry_url/tinygallery-backend:latest
```

### Run the Docker container:

```shell
docker run -p 8000:8000 -v "./admin_list.json:/app/admin_list.json" -d your_registry_url/tinygallery-backend:latest
```

## Configuration

The configuration for the backend is stored in the `.env` file. The default values should be sufficient for local development, but you may need to modify them if you're deploying the backend to a production environment.

## Deployment

To deploy the backend, you can follow these steps:

* Modify the values in the `.env` file to match your deployment environment.
* Install the required dependencies by running `pip install -r requirements.txt`.
* Launch the backend server using a process manager like `systemd`, `supervisor`, or `pm2`.

## Conclusion

That's it! You should now have a working instance of the TinyGallery Backend up and running. Use this README as a guide to get started with running and deploying the backend.


