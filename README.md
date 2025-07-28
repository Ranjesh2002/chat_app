# 🧠 FastAPI Chat Application – Internship Task (Brahmabyte Lab)

This project is a real-time WebSocket-based chat application built using **FastAPI** and **PostgreSQL**. It features JWT-based authentication and role-based access control (RBAC). Messages are stored in a PostgreSQL database and broadcasted in real-time via WebSockets.

---

## ✅ Features

- 🔐 **JWT Authentication** – Login system with hashed passwords
- 👥 **Role-Based Access Control (RBAC)** – Separate access for `admin` and `user`
- 💬 **WebSocket Chat** – Token-protected endpoint for real-time messaging
- 🗃️ **PostgreSQL Persistence** – Store messages and user data
- 🧱 **Clean structure** – Organized FastAPI modules with SQLAlchemy models

---

## 🚀 How to Run the Project

### 1. Setup Python Virtual Environment

```bash
git clone <repo-url>
cd chat-app
python -m venv venv
# Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
