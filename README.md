# Wedding Management System

A full-stack Django + PostgreSQL application for managing weddings end-to-end: couples, clients, guests, services, budgets/payments, and event planning. Ships with a custom dashboard, an elegant wedding-themed UI, and Django Admin.

## Features

- **Authentication** — admin login/logout, secure sessions, `@login_required` on every CRUD page.
- **Dashboard** — total weddings, clients, guests, services, payments; global budget overview; upcoming weddings and upcoming planning events; recent payments.
- **Weddings** — full CRUD (bride / groom / date / location / status / budget / notes).
- **Clients** — full CRUD, each client linked to a wedding with a role (bride, groom, parent, planner, other).
- **Guests** — full CRUD with RSVP status (pending / confirmed / absent) and plus-one count.
- **Services** — full CRUD across categories (venue, catering, decoration, photography, music, other) with status tracking.
- **Budget & Payments** — per-wedding total budget, paid amount, remaining amount, full payment history.
- **Planning / Schedule** — per-wedding event list (title, date, time, location, notes).
- **Admin** — every model registered with list filters, search, autocomplete on FKs, date hierarchies.
- **UI** — responsive layout, sidebar navigation, dashboard cards, filterable data tables, clean form pages with validation, wedding-themed color palette (blush, rose, cream, gold).

## Tech stack

- Python 3.10+ / Django 5.0
- PostgreSQL (with a SQLite fallback via `USE_SQLITE=1` for quick demos)
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
│   └── <app>/…              # list / form / detail / delete per app
└── static/
    ├── css/style.css       # Wedding-themed styling
    └── js/app.js           # Sidebar toggle, alert auto-dismiss, confirms
```

## Database schema

All non-user models live in their own app and use Django's ORM.

```
Wedding (1) ── (N) Client
Wedding (1) ── (N) Guest
Wedding (1) ── (N) Service
Wedding (1) ── (N) Payment ─(N) ── (1) Service   (service is optional)
Wedding (1) ── (N) PlanningEvent
```

Full field list lives in `<app>/models.py` and `<app>/migrations/0001_initial.py`.

---

## Local setup

You only need two things to run the project locally: **Python 3.10+** and **pip**. PostgreSQL is recommended for production-like behavior, but there's a one-flag SQLite fallback if you just want to look around.

### 1. Clone and enter the project

```bash
git clone https://github.com/abderahmane-code/wedding-management-system.git
cd wedding-management-system
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create your `.env`

```bash
cp .env.example .env
```

Open `.env` and set the values you care about. Every key and what it does:

| Variable | Purpose | Required? |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Secret key for sessions/CSRF. Generate a strong one (see below). | Yes |
| `DJANGO_DEBUG` | `True` in dev, `False` in production. | Yes |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames (`localhost,127.0.0.1` in dev). | Yes |
| `TIME_ZONE` | IANA zone, e.g. `UTC`, `Africa/Nouakchott`, `Europe/Paris`. | Yes |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Postgres credentials (only used if `USE_SQLITE` is **not** set). | If using Postgres |
| `POSTGRES_HOST` / `POSTGRES_PORT` | Defaults to `localhost:5432`. | No |
| `USE_SQLITE` | Set to `1` to bypass Postgres and use a local `db.sqlite3` file. | No |

Generate a secret key quickly:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Pick a database: PostgreSQL (recommended) **or** SQLite (fast start)

<details open>
<summary><b>Option A — PostgreSQL (recommended)</b></summary>

**Install PostgreSQL:**

- **Ubuntu / Debian:**
  ```bash
  sudo apt-get update
  sudo apt-get install -y postgresql postgresql-contrib
  sudo systemctl enable --now postgresql
  ```
- **macOS (Homebrew):**
  ```bash
  brew install postgresql@16
  brew services start postgresql@16
  ```
- **Windows:** use the installer from <https://www.postgresql.org/download/windows/>.

**Create the database and user** (values must match your `.env`):

```bash
sudo -u postgres psql <<'SQL'
CREATE DATABASE wedding_db;
CREATE USER wedding_user WITH ENCRYPTED PASSWORD 'wedding_password';
GRANT ALL PRIVILEGES ON DATABASE wedding_db TO wedding_user;
ALTER DATABASE wedding_db OWNER TO wedding_user;
SQL
```

> On macOS Homebrew, Postgres runs as your user — drop the `sudo -u postgres` prefix and just run `psql postgres <<'SQL' … SQL`.

**Verify the connection** before running migrations:

```bash
PGPASSWORD=wedding_password psql -h localhost -U wedding_user -d wedding_db -c '\conninfo'
```

Leave `USE_SQLITE` **unset** (or commented out) in `.env`.

</details>

<details>
<summary><b>Option B — SQLite (zero-setup demo)</b></summary>

Add this single line to `.env` and skip the Postgres section entirely:

```env
USE_SQLITE=1
```

A `db.sqlite3` file will be created next to `manage.py` automatically on first migration.

</details>

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Run the dev server

```bash
python manage.py runserver
```

Open **<http://127.0.0.1:8000/>**. You'll be redirected to `/accounts/login/` — sign in with your superuser and you'll land on the dashboard.

### 8. (Optional) Collect static files (needed for production)

```bash
python manage.py collectstatic --noinput
```

---

## Key URLs

| URL | What it is |
| --- | --- |
| `/` | Redirects to dashboard (or login if anonymous) |
| `/accounts/login/`, `/accounts/logout/` | Auth |
| `/dashboard/` | Custom dashboard with counts, budget overview, upcoming events, recent payments |
| `/weddings/`, `/weddings/new/`, `/weddings/<id>/` | Wedding list / create / detail |
| `/clients/`, `/guests/`, `/services/`, `/payments/`, `/planning/` | Same list / create / detail / edit / delete pattern per app |
| `/admin/` | Django Admin (every model registered) |

Deep-link shortcuts used by the wedding detail page: `/services/new/?wedding=<id>`, `/clients/new/?wedding=<id>`, etc. — the wedding is preselected in the form.

## Development notes

- Form styling is centralized in `core/forms.py` via `StyledModelForm` (applies `form-control` / `form-select` classes automatically).
- Sidebar navigation is driven by `core.context_processors.sidebar_nav`; add a new module by appending to its items list.
- Dashboard aggregates use `Count(...)` / `Sum(...)` on the related managers — see `core/views.py`.
- `Wedding.remaining_amount = total_budget − total_paid` (sum of `Payment.amount`). Services alone do **not** reduce Remaining — only recorded payments do. This matches the "paid vs budget" framing.
- Role-based access can later be layered on top of `LoginRequiredMixin`: each view already goes through the login wall, so restricting by group/permission is a one-line change per view.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `django.db.utils.OperationalError: could not connect to server` on `migrate` | Postgres isn't running or credentials don't match `.env`. Either `sudo systemctl start postgresql` (or `brew services start postgresql@16`) and re-check `.env`, or temporarily set `USE_SQLITE=1` in `.env` and retry. |
| `psycopg.errors.InsufficientPrivilege` on `migrate` | The Postgres user doesn't own the database. Re-run the `ALTER DATABASE … OWNER TO wedding_user;` line from step 4. |
| CSS looks unstyled after `collectstatic` in production | Make sure `DJANGO_DEBUG=False` triggered `collectstatic` and that the web server is serving `staticfiles/`. |
| Dashboard shows everything as 0 after data exists | Verify you're logged in as the **same** user who created the records (no RLS, but sanity check); then confirm records actually exist via `/admin/`. |

## License

MIT (or adjust as needed for your organization).
