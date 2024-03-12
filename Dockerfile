FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_HOME=/bin/poetry
ENV PATH="${POETRY_HOME}/bin/:${PATH}"

EXPOSE 9000

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install bash python3 python3-dev postgresql-client  && \
    rm -vrf /var/cache/apk/* && \
    curl -sSL https://install.python-poetry.org  | python - && \
    poetry config virtualenvs.create false --local
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

COPY . .

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
WORKDIR $APP_HOME

ENTRYPOINT code/python manage.py migrate & code/python manage.py csu & code/python manage.py runserver 0.0.0.0:8000