# Messaging & Inbox Module — Feature Branch

**Branch:** `feature/messaging-notifications`
**Developer:** Rajveer Singh
**Module Responsibility:** Messaging + Notifications + Admin Integration

---

## 📌 Overview

This branch implements the **private messaging system** for the Social Media Application.

The goal of this module is to allow authenticated users to:

* View conversations (Inbox)
* Start new conversations
* Send messages between users
* View chat history

Notifications will be implemented in a later phase.

---

## ✅ Features Implemented

### 1️⃣ Authentication Integration

* Uses custom user model from `users` app
* Login required for all messaging routes
* Compatible with Auth system (`feature/auth-system`)

---

### 2️⃣ Inbox System

Users can:

* View conversation list
* Open chats with other users
* Navigate between chats

URL:

```
/messages/inbox/
```

---

### 3️⃣ Chat System

Conversation between two users includes:

* Message history ordered by timestamp
* Message sending form
* Real-time conversation persistence (database stored)

URL:

```
/messages/chat/<user_id>/
```

---

### 4️⃣ Send Message Page

Users can start a new conversation by selecting another registered user.

URL:

```
/messages/send/
```

---

## 🗂️ App Structure

```
messaging/
│
├── models.py        # Message model
├── views.py         # Inbox, Chat, Send message views
├── urls.py          # Messaging routes
├── templates/
│   └── messaging/
│       ├── inbox.html
│       ├── chat.html
│       └── send_message.html
```

---

## 🧱 Database Models

### Message Model

Fields:

* sender (ForeignKey → CustomUser)
* receiver (ForeignKey → CustomUser)
* content (Text)
* timestamp (auto created)

---

## ▶️ How To Run This Branch

```bash
git checkout feature/messaging-notifications
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then open:

```
http://127.0.0.1:8000/messages/inbox/
```

---

## ⚠️ Current Limitations

* Notifications temporarily removed (will be reintroduced later)
* No real-time WebSocket messaging yet
* Basic UI (frontend polish pending merge with auth frontend)

---

## 🔜 Planned Improvements

* Notification system
* Read/Unread messages
* Real-time messaging (Django Channels)
* Chat UI improvements
* Message search

---

## 🤝 Integration Notes (For Teammates)

This branch is designed to merge with:

```
feature/auth-system
```

Requirements before testing:

* Custom User Model must be active
* Authentication routes enabled

---

## ✅ Current Status

✔ Messaging system functional
✔ Database stable
✔ Compatible with authentication system
🚧 Notifications postponed

---

**Maintained by:** Rajveer (Messaging Module)
