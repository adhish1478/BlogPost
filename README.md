# BlogWorld

BlogWorld is a minimalistic Medium-inspired blogging platform built with Django and Vanilla JavaScript. It features a clean and responsive UI, user authentication, post creation, liking, commenting, and dynamic interactions using AJAX.

## Live site link: https://blogpost-qyzf.onrender.com/
##### ( This is a test site, might encounter some errors)
---

## 🚀 Features

- ✅ User registration & login using JWT
- ✅ Create, read, update, delete (CRUD) blog posts
- ✅ Like/unlike posts dynamically via AJAX
- ✅ View full post with comments and list of users who liked it
- ✅ Inline comment creation, edit, delete with live updates
- ✅ Responsive design using Bootstrap 5
- ✅ Reusable template components (navbar, modals, etc.)
- ✅ Dynamic navbar behavior based on login state
- ✅ Live search for blog posts

---

## 🔗 API Documentation

👉 Full Postman API Docs: [View on Postman](https://.postman.co/workspace/My-Workspace~8e7b8a38-01f1-4a3d-8da1-2f2a76c9c0f4/collection/12390328-1fa6e1d0-e226-4e51-b795-b5d39e493358?action=share&creator=12390328)  


---

## 🛠️ Tech Stack

| Layer     | Technology                     |
|-----------|--------------------------------|
| Backend   | Django, Django REST Framework  |
| Frontend  | Vanilla JavaScript, Bootstrap 5|
| Auth      | JWT (SimpleJWT)                |
| Database  | PostgreSQL                     |

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/BlogPost.git
cd BlogPost
```

### 2. Set-up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Installing Packages

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

create a .env file in root directory:
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5432/blogdb
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000
```

### 5. Run Migrations & Start Server

```bash
python manage.py migrate
python manage.py runserver
```

⸻

### Folder Structure

backend/
├── blogs/
│   ├── templates/blogs/
│   ├── static/blogs/
│   ├── views.py, models.py, urls.py
├── users/
│   ├── authentication views, serializers
├── backend/
│   ├── settings.py
├── staticfiles/               # for production after collectstatic
├── templates/
│   └── blogs/_navbar.html
├── requirements.txt
└── .env


⸻

### Authentication Flow
	•	Uses JWT (SimpleJWT)
	•	Access/refresh tokens stored in localStorage
	•	Auto-injects tokens into authenticated requests
	•	Logout triggers backend token blacklist and clears localStorage

⸻


### Deployment Ready

#### Collect static files for production:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```
#### Use .env variables like:
```bash
DATABASE_URL=postgres://user:pass@render-host:5432/db
SECRET_KEY=your_prod_secret
DEBUG=False
```
#### Set gunicorn backend.wsgi as the Render/Railway deploy command

⸻

Author

Adhish Aravind
🔗 GitHub: github.com/adhish14
📧 Email: adhish.aravind7@gmail.com

⸻


