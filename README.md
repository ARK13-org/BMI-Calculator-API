# BMI Calculator API

A RESTful backend for a BMI (Body Mass Index) Calculator application, built with **FastAPI** and **SQLAlchemy**. It provides user authentication, BMI measurement tracking, health statistics, goal management, and personalized settings.

## Features

- **User Authentication** — User registration and login with JWT-based authentication.
- **User Profiles** — Retrieve and update personal profile information.
- **BMI Calculation** — Calculate BMI and determine the corresponding health category.
- **BMI History** — Save, retrieve, update, and delete BMI measurements.
- **BMI Comparison** — Compare the latest measurement with previous records.
- **Statistics** — Access BMI statistics and measurement insights.
- **Goal Management** — Create, view, update, and delete personal goals.
- **Goal Progress** — Track progress toward personal goals.
- **User Settings** — Manage application preferences.
- **Dashboard** — Retrieve summarized information for the application dashboard.
- **Interactive API Documentation** — Explore and test endpoints through Swagger UI.

## Technologies

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **JWT Authentication**
- **Uvicorn**

## Project Structure

```text
BMI-Calculator-API/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── bmi.py
│   │   │   ├── dashboard.py
│   │   │   ├── goals.py
│   │   │   ├── settings.py
│   │   │   └── users.py
│   │   └── deps.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ARK13-org/BMI-Calculator-API.git
cd BMI-Calculator-API
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

Example configuration:

```env
APP_NAME=BMI Calculator API
API_V1_PREFIX=/api/v1
DATABASE_URL=sqlite:///./bmi_calculator.db
SECRET_KEY=your-secure-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500
```

**Important:** Replace the example secret key with a secure, randomly generated value. Never commit your actual `.env` file or production secrets to GitHub.

### 5. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

You can explore endpoints, provide request data, and test API functionality directly from Swagger UI.

## API Endpoints

All API routes use the `/api/v1` prefix.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new account |
| POST | `/auth/login` | Authenticate a user |

### Users

| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/profile` | Retrieve user profile |
| PATCH | `/users/profile` | Update user profile |

### BMI

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bmi/calculate` | Calculate BMI |
| GET | `/bmi/records` | Retrieve BMI history |
| POST | `/bmi/records` | Create a BMI record |
| PATCH | `/bmi/records/{id}` | Update a BMI record |
| DELETE | `/bmi/records/{id}` | Delete a BMI record |
| GET | `/bmi/latest` | Retrieve latest BMI record |
| GET | `/bmi/compare` | Compare BMI measurements |
| GET | `/bmi/statistics` | Retrieve BMI statistics |

### Goals

| Method | Endpoint | Description |
|---|---|---|
| GET | `/goals` | Retrieve goals |
| POST | `/goals` | Create a goal |
| GET | `/goals/progress` | Retrieve goal progress |
| PATCH | `/goals/{id}` | Update a goal |
| DELETE | `/goals/{id}` | Delete a goal |

### Settings

| Method | Endpoint | Description |
|---|---|---|
| GET | `/settings` | Retrieve user settings |
| PATCH | `/settings` | Update user settings |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/dashboard` | Retrieve dashboard information |

*Note: Authentication is required for protected endpoints. Refer to `/docs` for the exact request and response schemas.*

## Database

The project uses **SQLite** as its default database, with SQLAlchemy handling database operations and ORM models.

The database URL can be configured through the `DATABASE_URL` environment variable.

## Frontend Integration

This API was developed to serve a Flutter-based BMI Calculator application.

The Flutter frontend communicates with the backend through REST API requests and supports:

- Account registration and login.
- Profile management.
- BMI calculations and measurement history.
- BMI charts and comparisons.
- Goal tracking.
- User preferences.

## License

This project is open-source. See the repository for licensing information.
