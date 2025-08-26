# Introduction to Django - Alx_DjangoLearnLab

This repository contains tasks for learning the basics of Django development, from setting up a project to creating models and working with the Django admin interface.  

## Repository Information
- **GitHub Repo**: `Alx_DjangoLearnLab`
- **Directory**: `Introduction_to_Django`

---

## 📘 Overview

The project introduces you to Django by covering:  
- Environment setup and project creation  
- Defining and interacting with models using Django ORM  
- CRUD operations in the Django shell  
- Configuring and customizing the Django admin interface  

---

## 📂 Project Structure

```

Introduction\_to\_Django/
│
├── LibraryProject/          # Main Django project folder
│   ├── **init**.py
│   ├── settings.py          # Project settings/configurations
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
├── bookshelf/               # App containing the Book model
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py
│   ├── models.py            # Book model definition
│   ├── views.py
│   └── migrations/          # Database migration files
│
├── manage.py                # CLI utility to manage project
│
├── create.md                # Documentation: Create operation
├── retrieve.md              # Documentation: Retrieve operation
├── update.md                # Documentation: Update operation
├── delete.md                # Documentation: Delete operation
└── CRUD\_operations.md       # Summary of all CRUD operations

````

---

## ▶️ How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/Introduction_to_Django
````

### 2. Create Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install django
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Visit the app at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 6. Access Admin Panel

Create a superuser:

```bash
python manage.py createsuperuser
```

Login at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## ✅ Tasks

1. **Introduction to Django Development Environment Setup**
2. **Implementing and Interacting with Django Models**
3. **Utilizing the Django Admin Interface**

---

## 🔑 Key Learnings

* How to set up and run a Django project
* Understanding project structure (`settings.py`, `urls.py`, `manage.py`)
* Using Django ORM for database operations
* Managing models via the Django admin interface

---

```


```
