# [Ecommerce Backend](http://3.144.124.187:8000/swagger/)
RESTFUL API for e-commerce paltform with multiple integrated modules.

## Table of Content
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Server Setup](#server-setup)
- [API Endpoints](#api-endpoints)

## Features
- CRUD operations on categories, orders, products.
- Register and login users.
- Authentication and authorization services.
- Custom permissions logic, ensuring secure and precise data manipulation.
- Testing using pytest for each app to ensure reliability and functionality.
- CI/CD pipeline using GitHub Actions.
- Cloud Deployment on AWS using docker.

## Tech Stack
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Postgresql](https://www.postgresql.org/)
- [Pytest](https://docs.pytest.org/en/7.4.x/)
- [Docker](https://www.docker.com/)
- [Github Actions](https://github.com/features/actions)
- [AWS](https://aws.amazon.com/)
- [Swagger](https://swagger.io/)
- [Postman](https://www.postman.com/)


## Server Setup
#### 1. Clone the repo
```bash
$ git clone https://github.com/Mohamad-Aboda/e-commerce.git
```

#### 2. Move to the project directory
```bash
$ cd e-commerce/
```

#### 3. Docker Setup
```bash
$ docker-compose up --build
```

#### 4. Now check http://localhost:8000/

## API Endpoints
```
  http://127.0.0.1:8000/swagger/
  http://127.0.0.1:8000/redoc/
```