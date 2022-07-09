FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN sudo apt install postgresql postgresql-contrib
RUN sudo systemctl start postgresql.service

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "psql" ]

CMD [ "postgres" ]