FROM python:3.9 AS build

ENV APP_CODE=/usr/src/app
RUN mkdir $APP_CODE
RUN mkdir $APP_CODE/staticfiles
RUN mkdir $APP_CODE/static
WORKDIR $APP_CODE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock $APP_CODE/
RUN pip install pipenv && pipenv install --system

COPY . $APP_CODE/
CMD python manage.py makemigrations && python manage.py migrate && echo yes | python manage.py collectstatic && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

