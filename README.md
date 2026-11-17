# REN Backend

Django REST API for Real Estate Nepal.

- Django 5.2 LTS + Django REST Framework
- JWT authentication with SimpleJWT
- SQLite for local development
- 2,211 seeded property listings

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data
python manage.py runserver 127.0.0.1:8000
```

- API: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin/
- Health check: http://127.0.0.1:8000/health/

## Demo accounts

| Role | Email | Password |
| --- | --- | --- |
| Admin / listing owner | `admin@ren.local` | `admin12345` |
| Buyer | `demo@ren.local` | `demo12345` |

OTP emails use the console backend when `EMAIL_HOST_PASSWORD` is empty. The
code is printed in the terminal, and exposed on the OTP screen while
`DEBUG=True`. Copy `.env.example` to `.env` to configure SMTP, a secret key,
allowed hosts and CORS origins.

## Seed data

```bash
python manage.py seed_data          # skip if listings already exist
python manage.py seed_data --fresh  # delete and re-import all listings
```

Imports `updated_data3.csv`, fixes its swapped latitude/longitude columns,
generates descriptions and attaches bundled sample photos.

## Tests

```bash
python manage.py test
```

The 10 API tests cover registration, OTP verification, login, listing CRUD,
permissions, image uploads, search and saved homes.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/auth/register/` | Create an account |
| `POST` | `/auth/login/` | Log in (returns JWTs) |
| `GET` | `/auth/sendotp/<user_id>/` | Send an OTP |
| `POST` | `/auth/verifyotp/<user_id>/` | Verify an OTP |
| `GET` | `/post/` | Paginated listings |
| `POST` | `/post/` | Create a listing (auth) |
| `GET` | `/post/<id>/` | Listing detail |
| `PATCH` | `/post/<id>/` | Update (owner only) |
| `DELETE` | `/post/<id>/` | Delete (owner only) |
| `POST` | `/post/search/` | Advanced search |
| `GET` | `/post/mine/` | Own listings |
| `GET` | `/post/recommendations/` | Personalised feed |
| `GET` | `/savedhome/<user_id>/` | Saved listings |
| `POST` | `/savedhome/<user_id>/<post_id>/` | Save a listing |
| `DELETE` | `/savedhome/<user_id>/<post_id>/` | Remove a saved listing |

Authenticated requests use:

```
Authorization: Bearer <access_token>
```
