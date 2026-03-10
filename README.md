# StudyBridge

A web platform that helps students connect with peer mentors for international study guidance, with a simple acceptance estimation calculator and structured messaging.

Built as a bachelor CS diploma project using Django, PostgreSQL, and Docker.

---

## Description

StudyBridge connects applicants planning to study abroad with student mentors who are already enrolled at universities in their target countries. Applicants can search for mentors by country, university, and field of study, start direct conversations, and use an acceptance estimation calculator to evaluate their academic profile.

Mentors can apply for a verified badge by submitting their student enrollment details for manual admin review.

---

## Core Features

| Feature | Description |
|---|---|
| Role-based accounts | Users sign up as **Applicant** or **Mentor**; separate dashboards per role |
| Mentor directory | Search and filter mentors by country, university, degree, major, and language |
| Direct messaging | Persistent one-on-one chat between applicants and mentors |
| Acceptance calculator | Rule-based weighted formula estimating admission likelihood |
| Mentor verification | Mentors submit enrollment details; admin approves/rejects via Django admin |
| Admin panel | Full Django admin for managing users, profiles, and verification requests |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 4.2 |
| Database | PostgreSQL 15 |
| Frontend | Bootstrap 5.3, Bootstrap Icons 1.11.3, Django Templates |
| Containerization | Docker, Docker Compose |
| WSGI server | Gunicorn (production-ready, included in requirements) |
| Environment | python-dotenv |

---

## Project Structure

```
studybridge/
├── accounts/               # Custom User model, signup, login, logout
│   ├── models.py           # User extends AbstractUser, adds `role` field
│   ├── forms.py            # SignupForm with role selection
│   ├── views.py            # signup_view, login_view, logout_view, redirect_by_role
│   └── urls.py
│
├── core/                   # Home, dashboards, mentor listing, calculator
│   ├── views.py            # home, applicant_dashboard, mentor_dashboard,
│   │                       # mentor_list, mentor_detail, calculator_view
│   ├── calculator.py       # Pure Python rule-based scoring formula
│   ├── forms.py            # CalculatorForm
│   └── urls.py
│
├── profiles/               # User profile models and edit views
│   ├── models.py           # ApplicantProfile, MentorProfile, VerificationRequest
│   ├── forms.py            # ApplicantProfileForm, MentorProfileForm, VerificationRequestForm
│   ├── views.py            # edit_applicant_profile, edit_mentor_profile, submit_verification
│   ├── admin.py            # Custom approve/reject admin actions for VerificationRequest
│   └── urls.py
│
├── chat/                   # Messaging system
│   ├── models.py           # Conversation, Message
│   ├── views.py            # start_chat, conversation_list, conversation_detail
│   ├── forms.py            # MessageForm
│   └── urls.py
│
├── studybridge/            # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/              # All Django HTML templates
│   ├── base.html           # Navbar, flash messages, footer
│   ├── home.html
│   ├── accounts/           # login.html, signup.html
│   ├── applicant/          # dashboard.html
│   ├── mentor/             # dashboard.html
│   ├── mentors/            # list.html, detail.html
│   ├── profiles/           # edit_applicant.html, edit_mentor.html, verification_request.html
│   ├── chat/               # conversation_list.html, conversation_detail.html
│   └── core/               # calculator.html
│
├── static/
│   └── css/custom.css      # Custom styles (CSS variables, hero, chat bubbles)
│
├── .env                    # Environment variables (not committed)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Setup

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- No local Python or PostgreSQL installation required — everything runs inside containers

### 1. Clone the repository

```bash
git clone <repository-url>
cd studybridge
```

### 2. Create the `.env` file

Copy the example and fill in your values:

```bash
cp .env.example .env
```

Or create `.env` manually:

```env
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=studybridge_db
DB_USER=studybridge_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

> **Important:** `DB_HOST=db` refers to the Docker Compose service name. Keep this value as `db` when running with Docker.

### 3. Build and start the containers

```bash
docker compose up -d --build
```

This starts:
- `db` — PostgreSQL 15 container (mapped to host port `5433`)
- `web` — Django development server on port `8000`

Wait for both containers to be healthy:

```bash
docker compose ps
```

### 4. Run database migrations

```bash
docker compose exec web python manage.py makemigrations accounts
docker compose exec web python manage.py makemigrations chat
docker compose exec web python manage.py migrate
```

> Run `makemigrations` for `accounts` and `chat` on first setup — their migration folders are not pre-generated.

### 5. Collect static files (optional for development)

Django serves static files automatically in `DEBUG=True` mode. For production use:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

### 6. Create a superuser (admin account)

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 7. Open the site

| URL | Description |
|---|---|
| http://localhost:8000 | Home page |
| http://localhost:8000/admin/ | Django admin panel |

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `studybridge_db` |
| `DB_USER` | PostgreSQL username | `studybridge_user` |
| `DB_PASSWORD` | PostgreSQL password | `yourpassword` |
| `DB_HOST` | Database host (service name in Docker) | `db` |
| `DB_PORT` | Database port inside container | `5432` |

---

## Docker Commands Reference

```bash
# Start containers
docker compose up -d

# Rebuild after code changes
docker compose up -d --build

# Stop containers
docker compose down

# View logs
docker compose logs -f web

# Run Django management commands
docker compose exec web python manage.py <command>

# Open a shell in the web container
docker compose exec web bash
```

---

## Creating Demo Users

After running migrations, create accounts via the signup page at `/accounts/signup/` or use the shell:

```bash
docker compose exec web python manage.py shell
```

```python
from accounts.models import User

# Create an applicant
User.objects.create_user("alice", "alice@example.com", "password123", role="applicant")

# Create a mentor
User.objects.create_user("bob", "bob@example.com", "password123", role="mentor")
```

---

## Pages Reference

| URL | View | Access |
|---|---|---|
| `/` | Home | Public |
| `/accounts/signup/` | Sign up | Public |
| `/accounts/login/` | Login | Public |
| `/accounts/logout/` | Logout | Authenticated |
| `/dashboard/applicant/` | Applicant dashboard | Applicant only |
| `/dashboard/mentor/` | Mentor dashboard | Mentor only |
| `/mentors/` | Mentor listing with search/filter | Public |
| `/mentors/<id>/` | Mentor detail page | Public |
| `/calculator/` | Acceptance calculator | Authenticated |
| `/chat/` | Conversation list | Authenticated |
| `/chat/<id>/` | Conversation detail | Participants only |
| `/profile/applicant/edit/` | Edit applicant profile | Authenticated |
| `/profile/mentor/edit/` | Edit mentor profile | Authenticated |
| `/profile/mentor/verify/` | Submit verification request | Mentor only |
| `/admin/` | Django admin | Staff/superuser |

---

## Models Reference

### `accounts.User`
Extends Django's `AbstractUser`. Adds a `role` field with three choices: `applicant`, `mentor`, `admin`. Helper methods: `is_applicant()`, `is_mentor()`, `is_admin_role()`.

### `profiles.ApplicantProfile`
OneToOne with `User`. Fields: `full_name`, `country`, `target_country`, `target_degree`, `intended_major`, `preferred_language`, `bio`. Created lazily on first dashboard visit.

### `profiles.MentorProfile`
OneToOne with `User`. Fields: `full_name`, `current_country`, `university_name`, `degree_level`, `major`, `year_of_study`, `languages`, `bio`, `is_verified`. Only mentors with `full_name`, `current_country`, `university_name`, and `major` filled in appear in the public listing.

### `profiles.VerificationRequest`
OneToOne with `User` (mentor). Fields: `university_name`, `student_id`, `note`, `status` (pending/approved/rejected), `submitted_at`, `reviewed_at`. One request per mentor at a time; rejected requests can be resubmitted.

### `chat.Conversation`
Two ForeignKeys to `User`: `applicant` and `mentor`. `unique_together` constraint prevents duplicate conversations between the same pair. Ordered by `updated_at` descending.

### `chat.Message`
ForeignKey to `Conversation` and `sender`. Fields: `text`, `timestamp`. Ordered by `timestamp` ascending.

---

## Acceptance Calculator

The calculator is a transparent, rule-based scoring tool — it uses no machine learning or external data.

**Inputs:**
- GPA (0.0–4.0 scale)
- English proficiency score (0.0–9.0 IELTS scale)
- Motivation strength (self-assessed, 1–10)
- Extracurricular activities (self-assessed, 1–10)
- Target country difficulty (Easy / Moderate / Hard / Very Hard)
- Target university competitiveness (Low / Medium / High / Very High)

**Formula:**

1. Each input is normalized to a 0–100 scale
2. A weighted average produces the base score:
   - GPA: 35%
   - English score: 30%
   - Motivation: 20%
   - Extracurricular: 15%
3. Flat penalties are subtracted based on difficulty:
   - Moderate country or university: −5 pts
   - Hard: −12 pts
   - Very Hard: −20 pts
4. Score is clamped to [0, 100] and rounded to one decimal

**Labels:**
- ≥76% → Strong Chance
- ≥56% → Good Chance
- ≥36% → Moderate Chance
- <36% → Low Chance

The result page shows the full breakdown (per-factor contributions, penalties, and final score) for transparency.

---

## Mentor Verification

Mentors can request a verified badge to build credibility with applicants.

**Flow:**
1. Mentor navigates to `/profile/mentor/verify/` and submits their university name, student ID, and an optional note.
2. The request is saved with `status = pending`.
3. An admin reviews the request in the Django admin panel at `/admin/profiles/verificationrequest/`.
4. The admin selects the request and uses the **"Approve selected requests"** or **"Reject selected requests"** bulk action.
5. On approval, `VerificationRequest.status` is set to `approved` and `MentorProfile.is_verified` is set to `True`.
6. Verified mentors appear with a green "Verified" badge on their public profile and in the mentor listing.

Rules:
- Pending requests cannot be resubmitted (the form is hidden while under review)
- Rejected requests can be resubmitted with updated information
- Verification does not involve document uploads or automated checks — it is a manual admin workflow

---

## Chat System

The chat system is a simple synchronous text messaging system — no WebSockets, no real-time updates.

**Flow:**
1. An applicant visits a mentor's profile page and clicks "Start Chat"
2. A `POST` request is sent to `/chat/start/<mentor_pk>/`, which creates a `Conversation` record (or retrieves the existing one)
3. The applicant is redirected to the conversation detail page
4. Both participants can send messages by submitting the text form
5. After each message, the page reloads (standard POST-Redirect-GET pattern)
6. Messages are displayed as chat bubbles (blue for the sender, gray for the other party)

Access control:
- Only applicants can initiate conversations
- Only the two participants can view or send messages in a conversation
- Any other user attempting to access a conversation URL receives a 404

---

## Future Improvements

These are optional enhancements for a production version — not required for the prototype:

- **Email notifications** — notify mentors when a new message arrives (Django's built-in email backend)
- **Unread message count** — badge on the Chats nav link showing unread messages
- **Mentor search pagination** — paginate results when the mentor list grows large
- **Profile photos** — allow mentors to upload a profile picture (`ImageField` + media storage)
- **WebSocket chat** — replace page-reload messaging with real-time updates using Django Channels
- **Public mentor profiles** — allow unauthenticated users to view mentor profiles without signing up
- **Password reset** — add Django's built-in password reset flow via email
- **Deployment config** — production `settings.py` with `DEBUG=False`, `STATIC_ROOT`, and a reverse proxy (Nginx + Gunicorn)
