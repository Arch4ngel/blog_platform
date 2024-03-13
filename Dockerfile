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

COPY . /code

WORKDIR /code


CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "collectstatic"]
CMD ["python", "manage.py", "runserver 0.0.0.0:8000"]
#ENTRYPOINT gunicorn -c ./config/gunicorn.py config.wsgi