# 📝 Note Taking API

A modern, feature-rich note-taking application built with **FastAPI** and **SQLite**, featuring user authentication, tag-based organization, and full-text search capabilities.


## ✨ Features

### Core Functionality
- 📝 **Complete CRUD Operations** - Create, Read, Update, and Delete notes
- 🏷️ **Tag Management** - Organize notes with multiple tags using many-to-many relationships
- 🔍 **Full-Text Search** - Search notes by keywords in title or content
- 👤 **User Authentication** - Secure JWT-based authentication system
- 🔐 **Password Security** - Bcrypt password hashing for secure storage
- 🎨 **Beautiful Web Interface** - Modern, responsive UI with gradient design
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices

### Technical Features
- ⚡ **Fast & Async** - Built with FastAPI for high performance
- 🗄️ **SQLAlchemy ORM** - Elegant database operations
- 🔒 **Secure by Design** - JWT tokens, password hashing, and user isolation
- 📚 **Interactive API Docs** - Auto-generated Swagger UI and ReDoc
- 🎯 **RESTful API** - Clean, well-structured endpoints

## 🚀 Live Demo

- **Web Interface**: [Coming Soon - Will be deployed]
- **API Documentation**: [Coming Soon - Will be deployed]

## 📸 Screenshots

### Login Page
Clean and modern authentication interface

### Notes Dashboard
Intuitive note management with tags and search

### API Documentation
Auto-generated interactive API documentation

## 🛠️ Technology Stack

**Backend:**
- FastAPI 0.109.0
- Python 3.9+
- SQLAlchemy 2.0.23
- SQLite
- Pydantic 2.5.0

**Authentication & Security:**
- JWT (JSON Web Tokens)
- Bcrypt password hashing
- OAuth2 with Bearer tokens

**Frontend:**
- HTML5
- CSS3 (Custom styling with gradients)
- Vanilla JavaScript
- Jinja2 templating

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/note-taking-api.git
cd note-taking-api
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

The server will start on `http://127.0.0.1:8000`

### 5. Access the Application

- **Web Interface**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/docs
- **Login Page**: http://127.0.0.1:8000/login
- **Register Page**: http://127.0.0.1:8000/register

## 📁 Project Structure
```
DevRoaks/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and startup
│   ├── auth.py              # Authentication utilities (JWT, password hashing)
│   ├── database.py          # Database configuration and connection
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # Database operations (CRUD + Search)
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── notes.py         # Note management endpoints
│       └── tags.py          # Tag endpoints
├── templates/
│   ├── index.html           # Main notes interface
│   ├── login.html           # Login page
│   └── register.html        # Registration page
├── static/
│   ├── css/
│   │   ├── style.css        # Main application styles
│   │   └── auth.css         # Authentication pages styles
│   └── js/
│       ├── app.js           # Main application logic
│       └── auth.js          # Authentication logic
├── notes.db                 # SQLite database (auto-generated)
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | ❌ |
| POST | `/auth/login` | Login and get JWT token | ❌ |
| GET | `/auth/me` | Get current user info | ✅ |

### Notes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/notes/` | Create a new note | ✅ |
| GET | `/notes/` | Get all notes (with optional tag filter) | ✅ |
| GET | `/notes/{id}` | Get a specific note | ✅ |
| PUT | `/notes/{id}` | Update a note | ✅ |
| DELETE | `/notes/{id}` | Delete a note | ✅ |
| GET | `/notes/search/` | Search notes by keyword | ✅ |

### Tags

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tags/` | Get all available tags | ✅ |

## 📖 Usage Examples

### Register a New User
```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "secure123"
  }'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secure123"
```

### Create a Note
```bash
curl -X POST "http://127.0.0.1:8000/notes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my note",
    "tag_names": ["work", "important"]
  }'
```

### Search Notes
```bash
curl -X GET "http://127.0.0.1:8000/notes/search/?q=meeting" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Filter Notes by Tag
```bash
curl -X GET "http://127.0.0.1:8000/notes/?tag=work" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🗄️ Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`

### Notes Table
- `id` (Primary Key)
- `title`
- `content`
- `user_id` (Foreign Key → Users)
- `created_at`
- `updated_at`

### Tags Table
- `id` (Primary Key)
- `name` (Unique)

### Note_Tags Table (Association)
- `note_id` (Foreign Key → Notes)
- `tag_id` (Foreign Key → Tags)

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **User Isolation**: Users can only access their own notes
- **Token Expiration**: 30-minute token lifetime
- **Input Validation**: Pydantic schemas for request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🎯 Key Highlights

1. **Clean Architecture**: Separation of concerns with routers, models, schemas, and CRUD operations
2. **Type Safety**: Full type hints with Pydantic validation
3. **Interactive Documentation**: Auto-generated Swagger UI for easy API testing
4. **User-Friendly Interface**: Beautiful gradient UI with smooth interactions
5. **Scalable Design**: Easy to extend with new features
6. **Production-Ready**: Proper error handling and security measures

## 🚧 Future Enhancements

- [ ] Note sharing between users
- [ ] Rich text editor support
- [ ] File attachments
- [ ] Note categories/folders
- [ ] Export notes (PDF, Markdown)
- [ ] Dark mode toggle
- [ ] Email notifications
- [ ] Two-factor authentication

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 License

This project is [MIT](LICENSE) licensed.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy for excellent ORM
- Inspiration from modern note-taking applications

---

⭐ **If you found this project helpful, please give it a star!** ⭐

Made with ❤️ and Python
```

---

## Short Tags for GitHub Topics:

Add these topics to your repository:
```
fastapi
python
rest-api
jwt
sqlalchemy
sqlite
authentication
note-taking
crud
api
web-app
pydantic
bcrypt
oauth2
```

---

## .gitignore File (Create this):

Create a file called `.gitignore` in your DevRoaks folder:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/