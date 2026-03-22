## Deployment Guide — AWS EC2

### First Time Setup
```bash
# SSH into server
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Clone repo
git clone https://github.com/YOUR_USERNAME/studybridge.git
cd studybridge

# Create .env file
cp .env.example .env
nano .env
# Fill in SECRET_KEY, DB credentials, DEBUG=False, ALLOWED_HOSTS=YOUR_IP

# Build and start
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Create superuser
docker compose exec web python manage.py createsuperuser
```

### Every Update After Git Push
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
cd studybridge
git pull origin main
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

### Verify ML Is Working
- Log in as an applicant
- Complete your profile with target country and major
- Visit the Mentors page
- You should see "AI Recommended Mentors" section with match scores
