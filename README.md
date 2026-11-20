# 📱 Synapse — Social Media Application (Django)

Synapse is a full-stack social media web application built using Django, inspired by modern platforms like Instagram.

The project focuses on **secure authentication**, **interactive social features**, and a **clean production-style UI**.  
It is designed as an industry-level portfolio project demonstrating backend architecture, authentication security, and modern social media functionality.

---

## ✨ Features

### 🔐 Authentication & Security
- Custom User Model
- Email verification before account activation
- Login using Username or Email
- Token-based Password Reset
- TOTP Two-Factor Authentication (2FA)
- Brute-force protection using Django Axes
- Secure cookie configuration
- Environment variable security using `.env`

### 📸 Social Media Features
- Create image posts with captions
- Instagram-style home feed
- Like / Unlike posts (AJAX — no page reload)
- Comment system
- Public user profiles
- Followers / Following system
- Delete own posts
- Messaging interface (UI implemented)

### 🎨 UI / UX
- Modern card-based layout
- Premium icon system (Font Awesome)
- Sidebar navigation
- Profile avatars
- Dark / Light theme support
- Instagram-inspired user experience

---

## 🛠 Tech Stack

| Category | Technology |
|---------|------------|
| Backend | Django 5.2 |
| Language | Python 3.10+ |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript |
| Authentication | django-axes, pyotp |
| Environment Config | python-dotenv |
| Icons | Font Awesome |

---

## 🚀 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/Social_Media_Application.git
cd social-media
```
### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create .env File

```bash
SECRET_KEY=your_secret_key_here
DEBUG=True

DB_NAME=social_media_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 5️⃣ Configure MySQL Database

Open MySQL and run:

```bash
CREATE DATABASE social_media_db;
```

### 6️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8️⃣ Run Development Server

```bash
python manage.py runserver
```

Open in browser:

```bash
http://127.0.0.1:8000/
```

---
## 📂 Project Structure (Simplified)

```bash
social_media/
│
├── users/        → authentication & profiles
├── posts/        → posts, likes, comments
├── messaging/    → chat system
├── templates/    → UI templates
├── static/       → CSS & assets
└── manage.py
```
---
## 🔒 Security Highlights
- Email activation required before login
- Two-Factor Authentication (TOTP QR verification)
- Login attempt protection (django-axes)
- Environment variable secrets
- CSRF protection enabled
---
## 🎯 Future Improvements
- Real-time notifications
- Stories feature
- WebSocket-based messaging
- Post saving/bookmark system
- Deployment with Docker & Cloud hosting
---
## 👨‍💻 Author
Rajveer Singh
B.Tech Computer Science Engineering (AI and ML) — 3rd Year

Portfolio Project — Django Social Media SaaS.
