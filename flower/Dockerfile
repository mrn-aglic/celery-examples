FROM mher/flower as flower

USER root

RUN mkdir /app && mkdir /config

COPY ./flower/flowerconfig.py /config/flowerconfig.py
RUN chmod +x /config/flowerconfig.py

COPY . /app

WORKDIR /app/

ADD ./requirements/*.txt /app/requirements/
RUN pip install -r requirements/requirements.txt

USER flower
