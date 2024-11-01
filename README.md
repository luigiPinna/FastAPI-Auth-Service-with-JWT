# FastAPI JWT Authentication Service

A FastAPI-based authentication service implementing JWT (JSON Web Tokens) with refresh token functionality and token blacklisting.

## 🚀 Features

- ✅ JWT Authentication
- ✅ Refresh Token System
- ✅ Token Blacklisting for logout
- ✅ PostgreSQL Database
- ✅ Configurable CORS
- ✅ Docker ready

## 🛠️ Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- Docker

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL
- Docker and Docker Compose (optional)

## 🔧 Installation

1. Clone the repository
```bash
git clone <your-repo-url>
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\\venv\\Scripts\\activate   # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`
```bash
cp .env.example .env
# Modify the variables in .env with your values
```

## 🐳 Docker Usage

1. Build and start containers
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## 🚀 Local Usage

1. Start the application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Authentication

#### Registration
```http
POST /auth/register
Content-Type: application/json

{
    'email': 'user@example.com',
    'name': 'User Name',
    'password': 'strongpassword'
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com
password=strongpassword
```

#### Refresh Token
```http
POST /auth/refresh
Authorization: Bearer <refresh-token>
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer <access-token>
```

## 📁 Project Structure

```
app/
├── api/
│   └── auth.py         # Authentication endpoints
├── core/
│   └── config.py       # Configuration settings
├── database/
│   └── session.py      # Database setup
├── models/
│   ├── base.py         # Base model
│   ├── token.py        # Token model
│   └── user.py         # User model
├── schemas/
│   ├── token.py        # Token schema
│   └── user.py         # User schema
└── main.py             # Entry point
```

## ⚙️ Environment Variables

Create a `.env` file with the following variables:

```env
# Base
PROJECT_NAME=FastAPI Auth Service
VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=['http://localhost:3000','http://localhost:8000']

# Database
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=fastapi
```

## 🔐 Security Features

- Password hashing using bcrypt
- Configurable JWT token expiration
- Refresh token system for enhanced security
- Token blacklisting for logout management
- Configurable CORS for allowed origins

## 🛡️ Authentication Flow

1. User registers with email and password
2. User logs in and receives access and refresh tokens
3. Access token is used for authenticated requests
4. Refresh token can be used to obtain new access tokens
5. Tokens can be blacklisted on logout for security

## 🔍 API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## 🧪 Development Features

- FastAPI's automatic API documentation
- SQLAlchemy ORM for database operations
- Pydantic models for request/response validation
- Asynchronous endpoint support
- Dependency injection system

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## 📝 License

[MIT](https://choosealicense.com/licenses/mit/)"

###---------------------------------------------------
###Italian Version
# FastAPI JWT Authentication Service

Un servizio di autenticazione basato su FastAPI che implementa JWT (JSON Web Tokens) con funzionalità di refresh token e blacklisting.

## 🚀 Caratteristiche

- ✅ Autenticazione JWT
- ✅ Refresh Token
- ✅ Token Blacklisting per logout
- ✅ Database PostgreSQL
- ✅ CORS configurabile
- ✅ Docker ready

## 🛠️ Tecnologie Utilizzate

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT
- Docker

## 📋 Prerequisiti

- Python 3.9+
- PostgreSQL
- Docker e Docker Compose (opzionale)

## 🔧 Installazione

1. Clona il repository
```bash
git clone <your-repo-url>
```

2. Crea un ambiente virtuale
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\\venv\\Scripts\\activate   # Windows
```

3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

4. Crea un file `.env` basato su `.env.example`
```bash
cp .env.example .env
# Modifica le variabili nel file .env con i tuoi valori
```

## 🐳 Utilizzo con Docker

1. Costruisci e avvia i container
```bash
docker-compose up --build
```

L'API sarà disponibile su `http://localhost:8000`

## 🚀 Utilizzo Locale

1. Avvia l'applicazione
```bash
uvicorn app.main:app --reload
```

L'API sarà disponibile su `http://localhost:8000`

## 📚 API Endpoints

### Autenticazione

#### Registrazione
```http
POST /auth/register
Content-Type: application/json

{
    'email': 'user@example.com',
    'name': 'User Name',
    'password': 'strongpassword'
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com
password=strongpassword
```

#### Refresh Token
```http
POST /auth/refresh
Authorization: Bearer <refresh-token>
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer <access-token>
```

## 📁 Struttura del Progetto

```
app/
├── api/
│   └── auth.py         # Endpoint autenticazione
├── core/
│   └── config.py       # Configurazioni
├── database/
│   └── session.py      # Setup database
├── models/
│   ├── base.py         # Base model
│   ├── token.py        # Token model
│   └── user.py         # User model
├── schemas/
│   ├── token.py        # Token schema
│   └── user.py         # User schema
└── main.py             # Entry point
```

## ⚙️ Variabili d'Ambiente

Crea un file `.env` con le seguenti variabili:

```env
# Base
PROJECT_NAME=FastAPI Auth Service
VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=['http://localhost:3000','http://localhost:8000']

# Database
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=fastapi
```

## 🔐 Sicurezza

- Le password sono hashate con bcrypt
- I token JWT hanno una scadenza configurabile
- Sistema di refresh token per una migliore sicurezza
- Blacklisting dei token per gestire il logout
- CORS configurabile per le origini permesse

## 🤝 Contribuire

Le pull request sono benvenute. Per modifiche importanti, apri prima un issue per discutere cosa vorresti cambiare.

## 📝 License

[MIT](https://choosealicense.com/licenses/mit/)