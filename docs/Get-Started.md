# Getting Started with TinyGallery Backend

This guide will help you set up and run the TinyGallery Backend on your local machine for development and testing purposes.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.6 or higher
- pip (Python package manager)
- Git

## Step 1: Clone the Repository

First, clone the TinyGallery Backend repository to your local machine:

```bash
git clone https://github.com/WeepingDogel/tinygallery-backend.git
cd tinygallery-backend
```

## Step 2: Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

## Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Create a `.env` file in the project root directory and add the following configuration:

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./database/database.sqlite
```

Replace `your_secret_key_here` with a secure random string.

## Step 5: Initialize the Database

Run the following command to initialize the database:

```bash
python -c "from app.model import models; from app.dependencies.db import engine; models.Base.metadata.create_all(bind=engine)"
```

## Step 6: Run the Development Server

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The server should now be running at `http://localhost:8000`.

## Step 7: Access the API Documentation

Open your web browser and go to `http://localhost:8000/docs` to view the Swagger UI documentation for the API.

## Next Steps

- Explore the API endpoints using the Swagger UI documentation.
- Set up the frontend application to interact with this backend.
- Read the full API documentation in the `docs/API-References.md` file.
- If you want to contribute to the project, check out the `CONTRIBUTING.md` file.

Congratulations! You now have the TinyGallery Backend running on your local machine.
