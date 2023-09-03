# <div align="center">BLOG API 🌐</div>

<div align="center">
<img src="assets/token.png" align="center" style="width: 100%; height: 40%" />
</div>

<br/>

I had a similar project written in Django, but I wanted to develop an API for it and decided to create a new project
using Django Rest Framework. I tried to fill this project with the necessary and modern technologies to build a
full-fledged Restful API project.

## Description

<div align="center">
<img src="assets/main.gif" align="center" style="width: 100%; height: 40%" />
</div>

<br/>

This project provides an API for a blog. Authorization is done using the popular JWT technology. You can view your
profile, see a list of all posts, as well as each post individually. In addition, you have access to post search. You
can leave comments on each post. To contact us, you can use a POST request at [this](http://127.0.0.1:8000/api/contacts)
link. For convenience, tags can be added to each post, which you can use to search for similar projects. Documentation
is provided for the entire project. You can download it by following [this](http://127.0.0.1:8000/api/schema) link or
view it in online format [here](http://127.0.0.1:8000/api/schema/redoc)
or [here](http://127.0.0.1:8000/api/schema/swagger-ui).

## Technologies

***Languages***

![Python](https://img.shields.io/badge/-Python-1C1C1C?&style=for-the-badge)

***Framework***

![Django](https://img.shields.io/badge/-Django-1C1C1C?&style=for-the-badge)

***Databases***

![Postgres](https://img.shields.io/badge/-Postgresql-1C1C1C?&style=for-the-badge)
![Redis](https://img.shields.io/badge/-Redis-1C1C1C?&style=for-the-badge)

***Libraries***

![Django-allauth](https://img.shields.io/badge/-Django--rest--framework-1C1C1C?&style=for-the-badge)
![aioredis](https://img.shields.io/badge/-django--taggit-1C1C1C?&style=for-the-badge)
![Redis](https://img.shields.io/badge/-django--redis-1C1C1C?&style=for-the-badge)
![Celery](https://img.shields.io/badge/-Celery-1C1C1C?&style=for-the-badge)
![psycopg2](https://img.shields.io/badge/-psycopg2-1C1C1C?&style=for-the-badge)
![simplejwt](https://img.shields.io/badge/-simplejwt-1C1C1C?&style=for-the-badge)
![ckeditor](https://img.shields.io/badge/-ckeditor-1C1C1C?&style=for-the-badge)
![drf-spectacular](https://img.shields.io/badge/-drf--spectacular-1C1C1C?&style=for-the-badge)

***Other***

![Docker](https://img.shields.io/badge/-Docker-1C1C1C?&style=for-the-badge)

To start with, I needed to implement user registration and authentication. As I mentioned earlier, I used JSON Web
Token (JWT) authentication, which is a modern and popular standard. Next, I worked on posts and implemented search,
pagination, and caching using Django's built-in methods. To manage tags, I used the Taggit library. I also integrated
Celery for asynchronous feedback submission. Finally, I documented my APIs using the Spectacular library.

## Project setup

***Method 1: Via docker-compose***

1. Create a .env file and paste the data from the .env.example file into it.
2. Generate django secret key on [this site](https://djecrety.ir/) and specify it in the SECRET_KEY variable.
3. Specify the user, password and name for the PostgreSQL and insert the values in the variables POSTGRES_USER,
   POSTGRES_PASSWORD, POSTGRES_DB.
4. Create an email and configure it to send messages. You can learn more about how to do
   this [here](https://youtu.be/dnhEnF7_RyM?t=902).
5. Run the project by entering following command:

```
docker-compose up -d --build
```

6. Perform migration to the database:

```
docker-compose exec web python manage.py migrate
```

7. Create a superuser by entering the following command:

```
docker-compose exec web python manage.py createsuperuser
```

8. You can log in to the [admin panel](http://0.0.0.0:8000/admin) and add new articles and comments or upload the
   fixtures I created by entering the command:

```
docker-compose exec web python manage.py loaddata core/fixtures/blog.json
```

***Method 2: Via virtual environment***

1. Create and activate a python virtual environment
2. In the terminal, enter the following command:

```
pip3 install -r requirements.txt
```

3. Create a .env file and paste the data from the .env.example file into it
4. The value of the variables POSTGRES_HOST and REDIS_HOST specify 'localhost'
5. Specify the user, password and name for the PostgreSQL and insert the values in the variables POSTGRES_USER,
   POSTGRES_PASSWORD, POSTGRES_DB.
5. Generate django secret key on [this site](https://djecrety.ir/) and specify it in the SECRET_KEY variable.
6. Create an email and configure it to send messages. You can learn more about how to do
   this [here](https://youtu.be/dnhEnF7_RyM?t=902).
8. Perform migration to the database:

```
python manage.py migrate
```

9. Create a superuser by entering the following command:

```
python manage.py createsuperuser
```

10. In the terminal, enter the following command:

```
python manage.py runserver
```

11. You can log in to the [admin panel](http://127.0.0.1:8000/admin) and add new articles and comments or upload the
    fixtures I created by entering the command:

```
python manage.py loaddata core/fixtures/blog.json
```

#### Remember that you must have PostgreSQL and Redis installed on your computer.

## <div align="center"> Thank you for taking the time to review my project! 👋</div>
