# Pinned, and nice lightweight image for python
FROM python:3.12.2-slim-bookworm

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential curl \
  # && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  # && apt-get install -y nodejs --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app

USER python

COPY --chown=python:python requirements*.txt ./

RUN pip install -r requirements.txt \
  && pip install -r requirements_dev.txt

ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python" \
    DBASIK_SECRET_KEY="yonklers"

COPY --chown=python:python . .

#RUN SECRET_KEY=nothing python manage.py collectstatic --no-input

CMD ["python", "manage.py", "runserver"] 
