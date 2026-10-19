# Django Login System

A Django-based user registration, login, and profile management application developed as part of the Consultadd Django Assignment.

## Features

- User registration with unique username and email
- Secure password hashing
- Login using email and password
- Login confirmation page
- Django Admin integration
- Database operations using Django ORM and Shell
- CRUD APIs for retrieving, updating, and deleting users
- API testing using Postman

## Technologies Used

Python, Django, SQLite, HTML, CSS, Postman, Git and GitHub.

## Project Structure

`LoginSystem/` — Main Django project configuration.

`Loginify/` — Django application containing models, views, forms, URLs, and templates.

`manage.py` — Django project management utility.

`requirements.txt` — Python dependencies.

## Installation and Setup

Create and activate a virtual environment:

```powershell
python -m venv DjangoAssignment
.\DjangoAssignment\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Apply database migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Application URLs

| URL | Description |
|---|---|
| `/` | Hello World page |
| `/signup/` | User registration |
| `/login/` | User login |
| `/confirmation/` | Login success page |
| `/admin/` | Django administration |

## CRUD API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/` | Retrieve all users |
| GET | `/api/users/by-email/?email=...` | Retrieve user by email |
| PUT | `/api/users/update/` | Update user information |
| DELETE | `/api/users/delete/?email=...` | Delete a user |

The APIs use Django sessions for authentication. Modifying requests require CSRF protection.

## Testing

Application functionality was tested using Django's development server, Django Shell, Django Admin, and Postman.

CRUD operations were verified using successful HTTP responses.

## Screenshots

Screenshots of the signup page, login page, login confirmation, Django Admin, and Postman API responses are included in the `screenshots/` directory.
