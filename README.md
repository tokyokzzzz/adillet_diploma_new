# StudyBridge

A web platform that helps students connect with verified peer mentors for international study guidance, powered by an AI recommendation engine and structured messaging.

Built as a bachelor CS diploma project using Django, PostgreSQL, and Docker. Deployed live on AWS EC2.

---

## Description

StudyBridge connects applicants planning to study abroad with verified student mentors enrolled at universities in their target countries. The platform uses an AI-powered recommendation engine to match applicants with the most relevant mentors based on profile similarity.

Mentors can apply for a verified badge by submitting their student enrollment details for manual admin review.

---

## Core Features

| Feature | Description |
|---|---|
| Role-based accounts | Users sign up as **Applicant** or **Mentor**; separate dashboards per role |
| Mentor directory | Search and filter mentors by country, university, degree, major, and language |
| Direct messaging | Persistent one-on-one chat between applicants and mentors |
| AI Mentor Recommendation | Content-based filtering using cosine similarity (scikit-learn). Recommends mentors ranked by compatibility score based on target country, university, field of study, and degree level. |
| Mentor verification | Mentors submit enrollment details; admin approves/rejects via Django admin |
| Admin panel | Full Django admin for managing users, profiles, and verification requests |
| Bilingual UI | Interface available in English and Kazakh, switchable at runtime |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 4.2 |
| Database | PostgreSQL 15 |
| Frontend | Bootstrap 5.3, Bootstrap Icons 1.11.3, Django Templates |
| Containerization | Docker, Docker Compose |
| WSGI server | Gunicorn |
| Environment | python-dotenv |
| Internationalization | Django i18n — English and Kazakh (Қазақша) |
| Source control | Git, GitHub |
| Cloud hosting | AWS EC2 (Ubuntu) |
| ML | scikit-learn, numpy, pandas |

---

## Machine Learning

### Algorithm
Content-Based Filtering — Cosine Similarity

### Library
scikit-learn (`sklearn.metrics.pairwise.cosine_similarity`)

### How It Works
1. Each mentor profile is encoded as a 4-dimensional feature vector: `[country, university, degree, major]`
2. The applicant profile is encoded using the same scheme
3. Cosine similarity measures the angle between vectors
4. Mentors are ranked by match score (0–100%)
5. Top matches are displayed on the mentor listing page and applicant dashboard

### Dataset
The dataset consists of user profiles stored in the platform PostgreSQL database. No external dataset or offline training phase is required. The system updates automatically as new mentors register.

### Why Cosine Similarity?
Cosine similarity is a standard technique for content-based recommendation systems. It is efficient, interpretable, and well-suited for categorical profile data. This approach is used in production systems by platforms like LinkedIn for people recommendations.

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
├── core/                   # Home, dashboards, mentor listing
│   ├── views.py            # home, applicant_dashboard, mentor_dashboard,
│   │                       # mentor_list, mentor_detail
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
│   └── core/               # (empty)
│
├── ml/                     # Machine learning recommendation engine
│   ├── __init__.py
│   ├── recommender.py      # get_mentor_recommendations() — cosine similarity
│   └── README_ML.md        # ML system documentation
│
├── locale/
│   ├── en/LC_MESSAGES/     # English translation files (django.po / django.mo)
│   └── kk/LC_MESSAGES/     # Kazakh translation files (django.po / django.mo)
│
├── static/
│   └── css/custom.css      # Custom styles (CSS variables, hero, chat bubbles)
│
├── .env                    # Environment variables (not committed)
├── .env.example            # Environment variable template
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

## Internationalization (i18n)

StudyBridge supports two languages switchable at runtime via Django's built-in i18n system.

| Language | Code | Status |
|---|---|---|
| English | `en` | Default |
| Kazakh | `kk` | Translated |

**Implementation details:**
- `django.middleware.locale.LocaleMiddleware` is active in the middleware stack
- `USE_I18N = True` and `LOCALE_PATHS = [BASE_DIR / "locale"]` in settings
- Translation files live in `locale/en/LC_MESSAGES/` and `locale/kk/LC_MESSAGES/` (`.po` source + compiled `.mo`)
- The `django.template.context_processors.i18n` context processor is enabled
- `gettext` system package is installed in the Docker image to support `makemessages` and `compilemessages`

**Django i18n commands (inside the container):**

```bash
# Extract strings marked for translation from templates and Python code
docker compose exec web python manage.py makemessages -l kk

# Compile .po files into binary .mo files (required after editing translations)
docker compose exec web python manage.py compilemessages
```

---

## GitHub

The project source code is hosted on GitHub and was used for deploying to the AWS EC2 server.

```bash
# Clone the repository
git clone https://github.com/<your-username>/studybridge.git
cd studybridge
```

Push changes to the server by pulling on the EC2 instance:

```bash
# On the EC2 server
cd ~/studybridge
git pull origin main
docker compose up -d --build
docker compose exec web python manage.py migrate
```

---

## AWS EC2 Deployment

StudyBridge is live and running on an AWS EC2 instance. The site is accessible via the server's public IP on port 8000.

### Infrastructure

| Component | Details |
|---|---|
| Cloud provider | AWS EC2 |
| OS | Ubuntu (latest LTS) |
| Runtime | Docker + Docker Compose |
| Source | Cloned from GitHub repository via SSH |
| Access | SSH with `.pem` key pair |

### How It Was Deployed

The server was provisioned on AWS EC2, accessed via SSH, and the application was deployed by cloning the GitHub repository directly onto the instance and running it with Docker Compose — the same setup used in local development.

**Steps performed:**

1. Launched an Ubuntu EC2 instance and configured inbound security group rules to allow ports `22` (SSH) and `8000` (Django)
2. Connected to the instance via SSH:
   ```bash
   ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
   ```
3. Installed Docker and Docker Compose on the server:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y docker.io docker-compose-plugin
   sudo usermod -aG docker ubuntu
   ```
4. Cloned the repository from GitHub:
   ```bash
   git clone https://github.com/<your-username>/studybridge.git
   cd studybridge
   ```
5. Created the `.env` file with production values (`DEBUG=False`, correct `ALLOWED_HOSTS`, secure credentials)
6. Built and started containers:
   ```bash
   docker compose up -d --build
   ```
7. Ran migrations, collected static files, and compiled translations:
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py collectstatic --noinput
   docker compose exec web python manage.py compilemessages
   ```
8. Created the superuser account for the admin panel

### Updating the Live Server

After pushing changes to GitHub, SSH into the server and pull:

```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
cd studybridge
git pull origin main
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

### Notes

- PostgreSQL data persists in the `postgres_data` Docker named volume — survives container restarts and rebuilds
- `STATIC_ROOT = BASE_DIR / "staticfiles"` is configured in settings; `collectstatic` works out of the box
- The `staticfiles/` directory is excluded from git via `.gitignore`
- The app runs directly on port `8000`; no Nginx reverse proxy is in place

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
- **Nginx reverse proxy** — put Nginx in front of Gunicorn for proper static file serving and SSL termination
