# TinyGallery Backend

TinyGallery Backend is a RESTful API built using FastAPI that powers the TinyGallery Vue Edition. It provides comprehensive functionality for managing images, posts, users, and more.

## Project Structure

- `app/`: Contains the main application code.
- `docs/`: Contains documentation for the project.

## Features

- User authentication and authorization
- Image upload and management
- Post creation and management
- Comment system
- Like functionality
- User profile management
- Admin panel for user and content management
- Avatar and background image customization

## Tech Stack

- Python 3.6+
- FastAPI
- SQLAlchemy (with SQLite)
- Pydantic for data validation
- JWT for authentication
- Pillow for image processing

## Getting Started

For detailed setup instructions, please refer to our [Get Started Guide](docs/Get-Started.md).

Quick start:

1. Clone the repository
2. Set up a virtual environment
3. Install dependencies
4. Configure environment variables
5. Initialize the database
6. Run the development server

```bash
git clone https://github.com/WeepingDogel/tinygallery-backend.git
cd tinygallery-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Configure .env file
python -c "from app.model import models; from app.dependencies.db import engine; models.Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the Swagger UI documentation at `http://localhost:8000/docs`.

For a more detailed API reference, see our [API Documentation](docs/API-References.md).

## Deployment

For information on deploying TinyGallery Backend to a production environment, please refer to our [Deployment Guide](docs/Deployment.md).

## Contributing

We welcome contributions to TinyGallery Backend! Please see our [Contributing Guide](CONTRIBUTING.md) for more details on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on our [GitHub Issues](https://github.com/WeepingDogel/tinygallery-backend/issues) page.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the awesome web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM
- All our contributors and users!
