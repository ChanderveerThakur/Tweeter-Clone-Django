# Tweeter Clone (Django + MongoDB + ImageKit)

A modern, responsive Twitter/X clone built with **Django 6**, **MongoDB** (via `django-mongodb-backend`), and **ImageKit.io Cloud Storage** for media uploads.

---

## Features
- **MongoDB Backend**: Powered by the official `django-mongodb-backend` with `ObjectIdAutoField` primary keys.
- **ImageKit Cloud Storage**: Automatic cloud media hosting with CDN delivery and dynamic thumbnail transformations.
- **Dynamic & Adaptive UI**: Mobile-first responsive design featuring a dark obsidian theme, frosted glass cards, mobile bottom navigation, and mobile floating action button (FAB).
- **Consolidated Templates**: All template views organized cleanly in a single `templates/` folder.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```ini
# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=True

# MongoDB Configuration (Local or MongoDB Atlas)
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_NAME=tweeter_db

# ImageKit Cloud Storage (https://imagekit.io/dashboard/developer/api-keys)
IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_imagekit_id
```

---

## Local Setup

1. **Clone repository**:
   ```bash
   git clone https://github.com/ChanderveerThakur/Tweeter-Clone-Django.git
   cd Tweeter-Clone-Django
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start server**:
   ```bash
   python manage.py runserver
   ```

---

## Deployment (e.g., Render)

1. **Create a Web Service** on [Render](https://render.com) linked to this repository.
2. **Build Command**:
   ```bash
   ./build.sh
   ```
3. **Start Command**:
   ```bash
   gunicorn tweeter.wsgi:application
   ```
4. **Environment Variables**:
   Add the following variables in the Render Dashboard:
   - `SECRET_KEY`: Generate a random secure key
   - `DEBUG`: `False`
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `MONGODB_NAME`: `tweeter_db`
   - `IMAGEKIT_PUBLIC_KEY`: Your ImageKit public key
   - `IMAGEKIT_PRIVATE_KEY`: Your ImageKit private key
   - `IMAGEKIT_URL_ENDPOINT`: Your ImageKit URL endpoint (e.g. `https://ik.imagekit.io/<id>`)
   - `CSRF_TRUSTED_ORIGINS`: `https://your-service-name.onrender.com`
