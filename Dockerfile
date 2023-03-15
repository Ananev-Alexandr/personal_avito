# 


FROM python:3.11

# 


WORKDIR /code

# 


COPY ./requirements.txt /code/requirements.txt

# 


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 


COPY ./app /code/app

# 


COPY ./.env_build  /code/.env

# 
COPY ./alembic  /code/alembic
COPY ./alembic.ini  /code/alembic.ini

# 
# RUN alembic init alembic

# RUN alembic upgrade head

#

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
