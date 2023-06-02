# pull official base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN 
COPY requirements.txt .
RUN pip install -r requirements.txt

# set work directory
WORKDIR /code

# copy project
COPY . .

EXPOSE 8080


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]