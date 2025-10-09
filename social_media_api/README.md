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

## API
### Follows & Feed API

#### Models
- `User.following` (ManyToMany to self) — users this user follows.
- `User.followers` (reverse relation) — users who follow this user.

#### Endpoints (authenticated)
- POST `/api/accounts/follow/<user_id>/` — Follow user (cannot follow yourself).
- POST `/api/accounts/unfollow/<user_id>/` — Unfollow user.
- GET `/api/accounts/users/<user_id>/followers/` — Get followers of a user.
- GET `/api/accounts/users/<user_id>/following/` — Get who a user is following.

#### Feed
- GET `/api/posts/feed/` — Returns posts from users the current authenticated user follows, ordered by `created_at` descending.

#### Example: follow with curl
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ \
-H "Authorization: Token <your_auth_token>"

#### Example: Fetch feed with curl
curl -X GET http://127.0.0.1:8000/api/posts/feed/ \
-H "Authorization: Token <your_auth_token>"

### Posts & Comments API
#### Models

Post: author, title, content, created_at, updated_at

Comment: post, author, content, created_at, updated_at

#### Endpoints (authenticated)

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/posts/ | GET | List all posts |
| /api/posts/ | POST | Create a new post |
| /api/posts/<post_id>/ | GET | Retrieve a single post |
| /api/posts/<post_id>/ | PUT/PATCH | Update a post (author only) |
| /api/posts/<post_id>/ | DELETE | Delete a post (author only) |
| /api/posts/<post_id>/comments/ | GET | List comments for a post |
| /api/posts/<post_id>/comments/ | POST | Add a comment to a post |
| /api/comments/<comment_id>/ | PUT/PATCH | Update a comment (author only) |
| /api/comments/<comment_id>/ | DELETE | Delete a comment (author only) |


#### Examples (curl)

##### Create a post:

curl -X POST http://127.0.0.1:8000/api/posts/ \
-H "Authorization: Token <your_auth_token>" \
-H "Content-Type: application/json" \
-d '{"title": "My First Post", "content": "Hello, world!"}'


##### Comment on a post:

curl -X POST http://127.0.0.1:8000/api/posts/1/comments/ \
-H "Authorization: Token <your_auth_token>" \
-H "Content-Type: application/json" \
-d '{"content": "Great post!"}'

### Likes API
#### Models

Like: user, post (each user can like a post only once)

Endpoints (authenticated)
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/posts/<post_id>/like/ | POST | Like a post |
| /api/posts/<post_id>/unlike/ | POST | Remove like from a post |


#### Examples (curl)

##### Like a post:

curl -X POST http://127.0.0.1:8000/api/posts/1/like/ \
-H "Authorization: Token <your_auth_token>"


##### Unlike a post:

curl -X POST http://127.0.0.1:8000/api/posts/1/unlike/ \
-H "Authorization: Token <your_auth_token>"

### Notifications API
#### Models

Notification: recipient, actor, verb, target (GenericForeignKey), timestamp

#### Endpoints (authenticated)
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/notifications/ | GET | Retrieve all notifications for the authenticated user |


##### Example (curl)

Get notifications:

curl -X GET http://127.0.0.1:8000/api/notifications/ \
-H "Authorization: Token <your_auth_token>"

## Deploying the Django REST API to Production

Objective: Deploy the API to a live environment with security and scalability.

Steps:

1. Prepare Project

   Set DEBUG=False, configure ALLOWED_HOSTS, security settings.

2. Choose Hosting Service

   Options: Heroku, AWS Elastic Beanstalk, DigitalOcean.

3.  Web Server & WSGI

    Use Gunicorn or uWSGI; optionally Nginx as a reverse proxy.

4.  Static & Media Files

    Configure collectstatic and media storage (e.g., AWS S3).

5. Deployment

   Push to GitHub, deploy using chosen provider, configure environment variables.

6. Monitoring & Maintenance

   Set up logging, monitoring, and regular updates.

7. Testing

   Validate endpoints on the live server.

### Deliverables:

- Deployment configuration files and scripts.

- Live URL of the deployed API.

- Documentation of deployment process and environment setup.

## Testing

- Use Postman for endpoint testing.

I- mplement automated tests for critical functionalities (authentication, posts, comments, likes, notifications).

- Ensure proper permissions and data validation across all endpoints.

## Repository Information

- GitHub Repository: Alx_DjangoLearnLab

- Project Directory: social_media_api

## Deployment
The Social Media API is deployed and publicly accessible at:
Live Demo: [https://elaines.pythonanywhere.com/](https://elaines.pythonanywhere.com/)



## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Heroku Deployment for Django](https://devcenter.heroku.com/articles/deploying-python)
- [AWS Elastic Beanstalk for Django](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [PythonAnywhere](https://www.pythonanywhere.com/)



