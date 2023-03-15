<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://upload.wikimedia.org/wikipedia/commons/7/75/Barter_System.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Personal Avito</h3>

<div align="center">

[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Ananev-Alexandr/personal_avito/pulls)

</div>

---


## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

The main goal of my project is to realize the possibility of a trading platform with numerous possibilities for users and administration. Implemented pagination, authorization with JWT-token

### Functionality for the user:
1) create advertisements
2) delete advertisements
3) leave a comment 
4) leave a complaint 
5) find ads by filter...

### Functionality for the admins:
1) all functionality available to users
2) banish and unbanish users
3) make admins
4) moving advertisements from one group to another
5) administrator's review of ad complaints
## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development.

**Must have python 3.11 installed**

**Installed Docker**
### Installing

A step-by-step series of examples on how to run a development environment 
# locally
Copying from the version control system
```
git copy https://github.com/Ananev-Alexandr/personal_avito.git
```
After that go to the downloaded project and create a virtual environment
```
python -m venv venv
```
After activate yor venv
```
venv\Scripts\activate

```
Now set the dependencies
```
pip install -r requirements.txt
```
Now we need to create our own **.env** file based on the **.env.example**

Starting the database in Docker

```
docker-compose up --build db-personal-avito
```
Doing the first database migration

```
alembic upgrade head
```

project launch

```
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
# launch with docker
You need to base **.env_build.example** and **.env.example** on **.env** and **.env_build**
```
docker-compose up --build db-personal-avito
```
```
docker-compose up --build run-migration
```
```
docker-compose up --build personal-avito
```



## 🎈 Usage <a name="usage"></a>

To work through OpenApi, you can at [Url](http://127.0.0.1:8001/docs#/): 

http://127.0.0.1:8001/docs#/

## ⛏️ Built Using <a name = "built_using"></a>

- [PostgreSQL](hhttps://www.postgresql.org/) - Database
- [FastAPI](https://fastapi.tiangolo.com/) - Web Framework
- [Docker](https://www.docker.com/) - Сontainer
- [SQLalchemy](https://www.sqlalchemy.org/) - ORM
- [Pydantic](https://docs.pydantic.dev/)

## ✍️ Authors <a name = "authors"></a>

- [@Ananev-Alexandr](https://github.com/Ananev-Alexandr)
