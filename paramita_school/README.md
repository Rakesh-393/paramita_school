# Paramita Heritage School — Django Project

## Tech Stack
- Python 3.11+ / Django 5.1
- MySQL Database
- Bootstrap 5.3 + Custom CSS (3D Animations)
- Font Awesome 6
- AOS (Animate on Scroll)

---

## Project Structure

```
paramita_school/
├── manage.py
├── requirements.txt
├── .env                        ← You create this (copy from .env.example)
├── paramita_school/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── home/
│   ├── models.py               ← All dynamic content models
│   ├── admin.py                ← Custom admin with image previews
│   ├── views.py
│   ├── urls.py
│   └── templates/home/
│       └── index.html          ← Full homepage template
├── static/
│   ├── css/style.css           ← 3D animations + full styling
│   └── js/main.js              ← Carousel + interactions
└── media/                      ← Uploaded images (auto-created)
```

---

## Step-by-Step Setup

### 1. Create & activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note for Windows:** If `mysqlclient` fails to install, download the wheel from:
> https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
> Then: `pip install mysqlclient‑2.x.x‑cpXX‑win_amd64.whl`

### 3. Create MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE paramita_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Create your .env file

```bash
cp .env.example .env
```

Edit `.env` with your actual MySQL credentials:

```
SECRET_KEY=django-insecure-replace-this-with-a-strong-random-key
DEBUG=True
DB_NAME=paramita_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

- **Homepage:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

---

## Admin Guide — What to Add First

Log in to `/admin/` and fill these in order:

| Section | Model | What to Add |
|---|---|---|
| 1 | **Site Settings** | Upload your school logo |
| 2 | **Nav Menu Items** | Add parent menu items, then child items |
| 3 | **Banner Slides** | Add 3–5 slides with image, title, subtitle, buttons |
| 4 | **Features** | Add 4 feature cards (icon, title, description) |
| 5 | **Introduction Section** | Heading, content, image |
| 6 | **About Section** | Heading, content, image |
| 7 | **Principal Message** | Name, photo, message text |
| 8 | **Testimonials** | Add parent/student reviews with star rating |
| 9 | **CTA Banner** | Enrollment CTA heading + button |
| 10 | **Social Feed Posts** | Upload Instagram/Facebook images |
| 11 | **Footer Information** | Address, phones, email, Google Map embed URL |

---

## Banner Slide Tips

- **Image size:** 1920 × 1080 px (landscape, high-res)
- Use the **Order** field to control slide sequence (0 = first)
- Toggle **Is Active** to show/hide slides without deleting them
- The carousel auto-plays every 6 seconds with 3D depth transitions

## Google Map Embed URL

1. Go to Google Maps → Search your school location
2. Click **Share → Embed a map → Copy HTML**
3. From the `<iframe>` tag, copy only the `src="..."` value
4. Paste it into **Footer → Map Embed URL**

---

## Production Deployment Checklist

```python
# In .env
DEBUG=False
SECRET_KEY=<strong-50-char-random-key>

# Collect static files
python manage.py collectstatic

# Set ALLOWED_HOSTS in settings.py
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```
