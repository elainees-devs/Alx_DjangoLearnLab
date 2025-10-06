# social_media_api (Alx_DjangoLearnLab)


## Setup


1. Create and activate a virtualenv (recommended).


2. Install requirements:


pip install -r requirements.txt


3. Create Django project and app (already provided in this repo):


django-admin startproject social_media_api
cd social_media_api
python manage.py startapp accounts


4. Update `settings.py`:
- Add `rest_framework`, `rest_framework.authtoken`, and `accounts` to INSTALLED_APPS.
- Set `AUTH_USER_MODEL = 'accounts.CustomUser'`.
- Configure `MEDIA_URL` and `MEDIA_ROOT` if you will upload profile images.


5. Make migrations and migrate:


python manage.py makemigrations
python manage.py migrate


6. Create a superuser (optional):


python manage.py createsuperuser


7. Run the server:


python manage.py runserver


8. Test endpoints using Postman or curl with the routes:
- POST /api/accounts/register/
- POST /api/accounts/login/
- GET/PUT /api/accounts/profile/ (authenticated)