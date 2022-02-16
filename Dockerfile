# a nice Dockerfile for Django projects - from https://londonappdeveloper.com/deploying-django-with-docker-compose/

# Pinned, and nice lightweight image for python
FROM python:3.9-alpine3.13
LABEL maintainer="yulqen"

ENV PYTHONDONTWRITEBYTECODE 1

# python outputs are sent straight to Docker logs
ENV PYTHONUNBUFFERED 1

# this tutorial uses a separate /app directory with the Django project
# but we're doing everything from the base directory
COPY ./requirements.txt /requirements.txt
COPY ./dbasik /app
COPY ./scripts /scripts

# set work directory, so that this is our working directory when running Docker commands
WORKDIR /app

# expose this for local development
EXPOSE 8000

# we break a run command into multiple lines so it does a lot and only adds one layer to the
# image. Here we are actually isolating our python in a virtualenv which we don't really need
# to do in Docker but probably nice for separation of concerns. Also a separate user for security reasons
# and to prevent us running everything in the container as root.
# The use of --virtual and .tmp-deps is all about installing what we need to get psycopg installed, then
# deleting those dependencies afterwards. This is totally optional but it follows the maxim of keeping
# things mimimal.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
      build-base postgresql-dev linux-headers musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]