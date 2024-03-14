# pull official base image
FROM python:3.12

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/bin/poetry
ENV PATH="${POETRY_HOME}/bin/:${PATH}"

EXPOSE 9000

# install dependencies
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install bash python3 python3-dev postgresql-client  && \
    rm -vrf /var/cache/apk/* && \
    curl -sSL https://install.python-poetry.org  | python - && \
    poetry config virtualenvs.create false --local
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

RUN python manage.py collectstatic --noinput

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "collectstatic"]
#CMD ["python", "manage.py", "runserver 0.0.0.0:8000"]
#ENTRYPOINT gunicorn -c ./config/gunicorn.py config.wsgi