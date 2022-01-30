FROM python:3.8
RUN apt-get update && apt-get install -y postgresql-contrib
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate
#RUN python3 manage.py create_superuser
#RUN python3 manage.py collectstatic
#RUN python3 manage.py runserver 0.0.0.0:8000
