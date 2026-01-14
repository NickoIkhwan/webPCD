# Deployment Guide for Smart Traffic Control System

## Pre-Deployment Checklist

### 1. Recommended Testing Method: GitHub Codespaces
The project is configured for **One-Click Testing** via GitHub:
- [ ] Push latest changes to GitHub.
- [ ] Open the repo in **GitHub Codespaces**.
- [ ] Run `python manage.py runserver`.
- [ ] Done! Dependencies and migrations are handled automatically.

### 2. Environment Setup (Standard Host)
- [ ] Copy `.env.example` to `.env`
- [ ] Update `.env` with your production values:

  - Generate a new SECRET_KEY (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
  - Set `DEBUG=False`
  - Add your domain to `ALLOWED_HOSTS`
- [ ] Add `.env` to `.gitignore` (NEVER commit it)

### 2. Database Migration
```bash
python manage.py migrate
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Create Superuser (if not already created)
```bash
python manage.py createsuperuser
```

### 5. Test Production Settings Locally
```bash
python manage.py runserver --insecure
```

## Deployment Platforms

### Option A: Railway / Render (Recommended for beginners)
1. Push code to GitHub
2. Connect repository to Railway/Render
3. Add environment variables in platform dashboard
4. Deploy automatically

### Option B: Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Option C: VPS (DigitalOcean, AWS, Linode)
1. SSH into your server
2. Clone repository
3. Set up virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` file
6. Run migrations
7. Use Gunicorn + Nginx:
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Security Checklist
- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is unique and not in version control
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] HTTPS enabled (use Let's Encrypt)
- [ ] Database backed up regularly
- [ ] Logs monitored for errors
- [ ] Admin panel (`/admin/`) protected or accessible only via VPN

## Important Notes
- **Model Files**: Ensure `myapp/media/model_4/model_4.pt` is included in deployment
- **Storage**: Consider cloud storage (AWS S3, Google Cloud Storage) for uploaded files
- **Database**: SQLite is not recommended for production; migrate to PostgreSQL
- **YOLO Processing**: May require GPU for production workloads; consider using cloud GPU services

## Troubleshooting
- If static files not loading: Run `python manage.py collectstatic`
- If database errors: Run `python manage.py migrate`
- If video processing fails: Check YOLO model path and GPU availability
