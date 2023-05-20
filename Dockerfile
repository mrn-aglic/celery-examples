FROM python:3.11-slim


RUN mkdir /app
WORKDIR /app/

ADD ./requirements/*.txt /app/requirements/

RUN apt-get -y update
RUN pip install --no-cache-dir -r requirements/requirements.txt

COPY . /app

LABEL name=celery-examples version=dev

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
