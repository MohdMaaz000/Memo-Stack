# MemoStack Backend

MemoStack is a high-performance RESTful backend API designed for structured note-taking and collaborative book annotations. It utilizes clean architecture and FastAPI to securely authenticate, create, read, update, and delete (CRUD) books, notes, and peer comments.

## 🚀 Features

- **User Authentication**: Secure login and registration system using JWT (Access & Refresh tokens) and bcrypt.
- **Book Management**: Add, update, delete, and organize personal books.
- **Note Management**: Create, edit, and delete notes associated with books.
- **Comment System**: Peer comments on notes.
- **Clean Architecture**: Services layer separation for business logic.
- **Performance & Security**: Rate limiting, global request logging, CORS configured, and PostgreSQL persistence.

## 🛠️ Tech Stack

- **Python 3.10+**: Runtime environment.
- **FastAPI**: High-performance web framework for building APIs.
- **SQLAlchemy & Alembic**: ORM and Database Migrations.
- **PostgreSQL / SQLite**: Support for both local SQLite development and production Postgres.
- **Pydantic**: Data validation and serialization.
- **PyTest**: Automated testing framework.

## 🚦 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/MohdMaaz000/Textmate.git
cd Textmate
```

### 2. Set up Virtual Environment and Install Dependencies

```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory based on standard configuration:

```ini
PROJECT_NAME="MemoStack API"
DATABASE_URL="sqlite:///./textmate.db" # Change to Postgres URI for production
SECRET_KEY="replace-with-a-very-secure-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### 4. Run Database Migrations

To create all necessary tables in your database:

```bash
alembic upgrade head
```

### 5. Start the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. 
Interactive Swagger API documentation is automatically generated and accessible at `http://localhost:8000/docs`.

## 🧪 Testing

To run the automated tests using PyTest:

```bash
pytest
```
