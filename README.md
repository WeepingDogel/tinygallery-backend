# TinyGallery Backend

TinyGallery Backend is a RESTful API built using FastAPI that powers the TinyGallery Vue Edition. It provides comprehensive functionality for managing images, posts, users, and more.

## Project Structure

- `app/`: Contains the main application code.
  - `dependencies/`: Dependency injection and database setup.
  - `model/`: Database models and schemas.
  - `routers/`: API route handlers.
  - `utilities/`: Utility functions and tools.
- `docs/`: Contains documentation for the project.
- `tests/`: Contains unit and integration tests.

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
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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

## CI/CD Pipeline

We use a comprehensive CI/CD pipeline to ensure code quality and automate the deployment process. For more details, see our [Pipeline Documentation](docs/pipeline.md).

## Contributing

We welcome contributions to TinyGallery Backend! Please see our [Contributing Guide](CONTRIBUTING.md) for more details on how to get started.

## Security

For information about our security policy and how to report security vulnerabilities, please see our [Security Policy](SECURITY.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on our [GitHub Issues](https://github.com/WeepingDogel/tinygallery-backend/issues) page.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the awesome web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM
- [Pillow](https://python-pillow.org/) for image processing
- All our contributors and users!
