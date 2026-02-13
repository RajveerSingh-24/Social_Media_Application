# Social Media Application (Django)

A production-grade social media authentication system built with Django.

This project includes:

- Custom User Model
- Email verification before activation
- Username or Email login
- Password reset (token-based)
- TOTP-based Two-Factor Authentication (2FA)
- Brute-force protection using Django Axes
- Secure cookie configuration
- MySQL database integration
- Environment variable configuration

---

## 🔧 Tech Stack

- Python 3.10+
- Django 5.2
- MySQL
- django-axes
- pyotp (2FA)
- qrcode
- python-dotenv

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-ORG/social-media.git
cd social-media

pip install -r requirements.txt
```

- SECRET_KEY=your_secret_key_here
- DEBUG=True

- DB_NAME=your_db_name
- DB_USER=your_db_user
- DB_PASSWORD=your_db_password
- DB_HOST=localhost
- DB_PORT=3306
- EMAIL_HOST_USER=your_email@gmail.com
- EMAIL_HOST_PASSWORD=your_app_password

```bash
Configure MySQL
CREATE DATABASE social_media_db;
python manage.py makemigrations
python manage.py migrate
```
## Run Development Server
```bash
python manage.py runserver
```

