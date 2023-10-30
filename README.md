<h1 align="center">Ecommerce</h1>

### Description

Ecommerce Project Still In Progress...

![-------------------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Local Setup 👨‍💻:

### 1.Virtual Environment Setup :

##### For Linux :

```
$. python3 -m venv env
$. source env/bin/activate
```

##### For Windows :

```
$. py -m venv env
$. env\Scripts\activate
```

![-------------------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

#### Installing Dependencies:

```
 pip install wheel
 pip install -r requirements.txt
```

![-------------------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

#### Create Database Tables and Superuser:

```
Note: For Windows Users Replace python3 with python

 python3 manage.py makemigrations
 python3 manage.py migrate
 python3 manage.py createsuperuser
```

![-------------------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### Run Server

```
 python3 manage.py runserver
```

![-------------------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### 2 Docker Setup :
```
 docker-compose up --build
```

### Access the endpoints :

http://localhost:8000/


### Endpoints

```
 http://127.0.0.1:8000/swagger/
 http://127.0.0.1:8000/redoc/

```

### Test Endpoints Live
```
http://13.59.210.23:8000/swagger/
```