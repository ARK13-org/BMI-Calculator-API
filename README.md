# BMI Calculator API

FastAPI backend for the BMI Calculator Flutter application.

## Features

- JWT authentication (register/login/current user)
- User profile management
- BMI calculation using adult reference categories
- Authenticated BMI measurement history (create/list/latest/update/delete)
- Date-filtered history, comparison, and trend statistics
- Weight goals and goal progress
- User settings (metric/imperial, notifications, theme)
- Dashboard summary
- Swagger UI at `/docs`
- SQLite by default; PostgreSQL can be configured through `DATABASE_URL`

> BMI is a screening measure, not a medical diagnosis. Adult BMI categories should not be applied to children and teens.

## 1. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for this terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure environment

```powershell
Copy-Item .env.example .env
```

Change `SECRET_KEY` in `.env` to a long random value before using the API beyond local development.

## 4. Run the API

Run from the project root:

```powershell
python -m uvicorn app.main:app --reload
```

- API root: http://127.0.0.1:8000/
- Swagger docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

The SQLite database is created automatically on first startup.

## Authentication

Register or log in through `/api/v1/auth/register` or `/api/v1/auth/login`. Copy the returned `access_token`, click **Authorize** in Swagger, and paste the token. The API uses HTTP Bearer authentication.

## Main endpoints

| Method | Endpoint | Auth |
|---|---|---|
| POST | `/api/v1/auth/register` | No |
| POST | `/api/v1/auth/login` | No |
| GET | `/api/v1/auth/me` | Yes |
| GET/PATCH | `/api/v1/users/profile` | Yes |
| DELETE | `/api/v1/users/account` | Yes |
| POST | `/api/v1/bmi/calculate` | No |
| POST | `/api/v1/bmi/records` | Yes |
| GET | `/api/v1/bmi/records` | Yes |
| GET | `/api/v1/bmi/latest` | Yes |
| GET | `/api/v1/bmi/compare` | Yes |
| GET | `/api/v1/bmi/statistics` | Yes |
| PATCH/DELETE | `/api/v1/bmi/records/{record_id}` | Yes |
| GET | `/api/v1/dashboard` | Yes |
| GET/POST | `/api/v1/goals` | Yes |
| PATCH/DELETE | `/api/v1/goals/{goal_id}` | Yes |
| GET | `/api/v1/goals/progress` | Yes |
| GET/PATCH | `/api/v1/settings` | Yes |

## Flutter connection notes

- Android emulator: use `http://10.0.2.2:8000/api/v1` (not `localhost`).
- Flutter web / desktop on the same computer: use `http://127.0.0.1:8000/api/v1`.
- Physical Android device: use your computer's LAN IPv4 address and allow port 8000 through the firewall.
- Send `Authorization: Bearer <access_token>` for protected endpoints.
- The current Flutter mock record model maps to `id`, `height_cm`, `weight_kg`, `bmi`, and `measured_at`. The API also returns `category` and `note`.

## Database changes

This starter uses SQLAlchemy `create_all` for initial local development. For future schema changes on an existing database, add Alembic migrations rather than expecting `create_all` to alter existing tables.
