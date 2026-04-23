# Wedding Management System

A full-stack Django + PostgreSQL application for managing weddings end-to-end: couples, clients, guests, services, budgets/payments, and event planning. Ships with a custom dashboard, an elegant wedding-themed UI, and Django Admin.

## Features

- **Authentication** — admin login/logout, 8-hour secure sessions, `@login_required` on every CRUD page.
- **Dashboard** — total weddings, clients, guests, services, payments; global budget overview; upcoming weddings and upcoming planning events; recent payments.
- **Weddings** — full CRUD (bride / groom / date / location / status / budget / notes).
- **Clients** — full CRUD, each client linked to a wedding with a role (bride, groom, parent, planner, other).
- **Guests** — full CRUD with RSVP status (pending / confirmed / absent) and plus-one count.
- **Services** — full CRUD across categories (venue, catering, decoration, photography, music, other) with status tracking.
- **Budget & Payments** — total budget per wedding, paid amount, remaining amount, full payment history (add / edit / delete).
- **Planning / Schedule** — per-wedding event list (title, date, time, location, notes).
- **Admin** — every model registered with list filters, search, autocomplete on FKs, date hierarchies.
- **UI** — responsive layout, sidebar navigation, dashboard cards, filterable data tables, clean form pages with validation, wedding-themed color palette (blush, rose, cream, gold).

## Tech stack

- Python 3.10+ / Django 5.0
- PostgreSQL (SQLite fallback available for quick testing via `USE_SQLITE=1`)
- Django templates + vanilla HTML / CSS / JavaScript
- `django-widget-tweaks`, `psycopg` (v3), `python-dotenv`

## Project structure

```
wedding-management-system/
├── manage.py
├── requirements.txt
├── .env.example
├── wedding_project/        # Django project (settings, urls, wsgi, asgi)
├── accounts/               # Login / logout (uses Django auth)
├── core/                   # Dashboard, context processors, shared forms
├── weddings/               # Wedding model + CRUD
├── clients/                # Clients linked to weddings
├── guests/                 # Guests + RSVP
├── services/               # Wedding services (venue, catering, …)
├── payments/               # Budget & payment history
├── planning/               # Planning / schedule events
├── templates/              # Global templates + base.html (sidebar layout)
│   ├── base.html
│   ├── accounts/login.html
│   ├── core/dashboard.html
│   ├── weddings/ …
│   ├── clients/ …
│   ├── guests/ …
│   ├── services/ …
│   ├── payments/ …
│   ├── planning/ …
│   └── includes/           # pagination + form partials
└── static/
    ├── css/style.css       # Wedding-themed styling
    └── js/app.js           # Sidebar toggle, alert auto-dismiss, confirms
```

## Database schema

All non-user models live in their own app and use Django's ORM. Relationships:

```
Wedding (1) ── (N) Client
Wedding (1) ── (N) Guest
Wedding (1) ── (N) Service
Wedding (1) ── (N) Payment ─(N) ── (1) Service   (service is optional)
Wedding (1) ── (N) PlanningEvent
```

Full field list is documented in `<app>/models.py` and visible in `migrations/0001_initial.py`.

## Step-by-step setup

### 1. Clone and enter the project

```bash
git clone <repo-url>
cd wedding-management-system
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and edit it:

```bash
cp .env.example .env
# Open .env and set DJANGO_SECRET_KEY, POSTGRES_* values
```

Key variables:

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key (required in production). |
| `DJANGO_DEBUG` | `True` for dev, `False` for production. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames. |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Database credentials. |
| `POSTGRES_HOST` / `POSTGRES_PORT` | Defaults to `localhost:5432`. |
| `USE_SQLITE=1` | Optional: use a local `db.sqlite3` file instead of PostgreSQL (handy for demos). |

### 4. Create the PostgreSQL database

```bash
sudo -u postgres psql <<'SQL'
CREATE DATABASE wedding_db;
CREATE USER wedding_user WITH ENCRYPTED PASSWORD 'wedding_password';
GRANT ALL PRIVILEGES ON DATABASE wedding_db TO wedding_user;
ALTER DATABASE wedding_db OWNER TO wedding_user;
SQL
```

Make sure these match the values in your `.env`.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. (Optional) Collect static files

```bash
python manage.py collectstatic --noinput
```

### 8. Run the dev server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/**. You will be redirected to `/accounts/login/`. Sign in with the admin account — you'll land on the dashboard.

Key URLs:

- `/` — redirects to dashboard or login
- `/dashboard/` — the custom dashboard
- `/weddings/`, `/clients/`, `/guests/`, `/services/`, `/payments/`, `/planning/` — module home pages
- `/admin/` — Django Admin (full access for superusers)

## Development notes

- Form styling is centralized in `core/forms.py` via `StyledModelForm` (applies `form-control` / `form-select` classes automatically).
- Sidebar navigation is driven by `core.context_processors.sidebar_nav`; add a new module by appending to its items list.
- Dashboard aggregates are computed with `Sum(...)` on the related managers — see `core/views.py`.
- Role-based access can later be layered on top of `LoginRequiredMixin`: each view already goes through the login wall, so restricting by group/permission is a one-line change per view.

## Running with SQLite (no PostgreSQL needed)

If you just want to try the app without installing PostgreSQL:

```bash
cp .env.example .env
echo "USE_SQLITE=1" >> .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## License

MIT (or adjust as needed for your organization).
