FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /code/
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py create_superuser
RUN #python manage.py collectstatic