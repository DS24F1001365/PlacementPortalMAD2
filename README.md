# Placement Portal Application (PPA)

A full-stack Placement Portal Application built using Flask, Vue.js, SQLite, Redis, Celery and MailHog.

---

## Tech Stack

### Backend
- Flask
- SQLite
- SQLAlchemy
- JWT Authentication
- Redis (Caching)
- Celery (Background Jobs)

### Frontend
- Vue.js
- Vue Router
- Bootstrap

### Additional Services
- Redis (Docker)
- MailHog (Docker)

---

# Features

## Authentication
- Admin Login
- Student Registration/Login
- Company Registration/Login
- JWT Authentication
- Role Based Authorization

## Admin
- Approve / Reject Companies
- Approve / Reject Drives
- Blacklist / Unblacklist Companies
- Dashboard Statistics
- View Students
- View Companies
- View Applications

## Company
- Company Profile
- Create Placement Drives
- Edit Placement Drives
- View Applications

## Student
- Student Profile
- Resume Upload
- Resume View
- Available Drives
- Apply for Drives
- View Applications
- Accept / Decline Offers

## Redis
- Dashboard API Caching
- Cache Expiry

## Celery Background Jobs
- CSV Export (Async)
- Daily Placement Reminder
- Monthly Placement Report

---

# Folder Structure

```
PlacementPortalApp/

│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── celery_app.py
│   ├── config.py
│   ├── cache_helpers.py
│   ├── mail_utils.py
│   ├── requirements.txt
│   ├── uploads/
│   ├── exports/
│   └── venv/ (Create after extracting ZIP)
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│
└── README.md
```

---

# Project Setup

After extracting the ZIP file, follow the steps below.

---

# 1. Open Docker Desktop

Start Docker Desktop and wait until Docker Engine is running.

---

# 2. Start Redis

Open PowerShell / Terminal and run

```bash
docker start redis-server
```

---

# 3. Start MailHog

```bash
docker start mailhog
```

---

# 4. Verify MailHog

Open

```
http://localhost:8025
```

MailHog Inbox should open.

---

# 5. Backend Setup

Open a new terminal.

Navigate to backend.

```bash
cd backend
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

The terminal should now display

```text
(venv)
```

---

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Flask Backend

```bash
python app.py
```

Backend runs at

```
http://127.0.0.1:5000
```

Leave this terminal running.

---

# 6. Start Celery Worker

Open another terminal.

Navigate to backend.

```bash
cd backend
```

Activate virtual environment.

```bash
venv\Scripts\activate
```

Run

```bash
celery -A celery_app.celery worker --loglevel=info
```

Leave this terminal running.

---

# 7. Start Celery Beat

Open another terminal.

Navigate to backend.

```bash
cd backend
```

Activate virtual environment.

```bash
venv\Scripts\activate
```

Run

```bash
celery -A celery_app.celery beat --loglevel=info
```

Leave this terminal running.

---

# 8. Frontend Setup

Open another terminal.

Navigate to frontend.

```bash
cd frontend
```

Install frontend dependencies.

```bash
npm install
```

Run frontend.

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

Open the above URL in the browser.

---

# Default Admin Credentials

Email

```
admin@ppa.com
```

Password

```
admin123
```

---

# Background Services

The following services must be running before using the application.

| Service | Purpose |
|----------|---------|
| Flask | Backend APIs |
| Vue | Frontend |
| Redis | Caching & Celery Queue |
| Celery Worker | Executes Background Jobs |
| Celery Beat | Executes Scheduled Jobs |
| MailHog | Receives Emails |

---

# Celery Background Jobs

## User Triggered Async Job

Student CSV Export

- Export Placement Applications
- Runs asynchronously
- CSV generated in background
- Download available after task completion

---

## Scheduled Job

Daily Placement Reminder

- Runs every day at configured time
- Sends reminder emails for upcoming placement deadlines
- Tested using MailHog

---

## Scheduled Job

Monthly Placement Report

- Runs on the first day of every month
- Sends placement statistics to Admin
- Tested using MailHog

---

# Redis Caching

The following APIs are cached using Redis.

- Admin Dashboard
- Company Dashboard
- Student Dashboard
- Student Available Drives

Cache timeout is configured in

```
config.py
```

---

# MailHog

MailHog receives all emails locally.

Open

```
http://localhost:8025
```

to view reminder emails and monthly reports.

---

# Notes

- Resume uploads are stored inside `backend/uploads/resumes/`.
- CSV exports are stored inside `backend/exports/`.
- Redis is used for caching and Celery message queue.
- Celery executes asynchronous and scheduled jobs.
- MailHog is used for local email testing.

---

# Development Notes

Temporary testing routes have been retained to simplify verification of scheduled Celery jobs during development and demonstration.

These routes can be used to manually trigger:

- CSV Export
- Daily Reminder
- Monthly Report

without waiting for the scheduled execution time.

---

# Shutdown

After the demo, stop the services.

Press **Ctrl + C** in

- Flask Terminal
- Celery Worker Terminal
- Celery Beat Terminal
- Vite Frontend Terminal

Docker containers may be stopped using

```bash
docker stop redis-server
docker stop mailhog
```

---

# Author

Harini Sailakshmi Chopperla

B.Tech Data Science

Placement Portal Application