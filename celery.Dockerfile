FROM python:3.8

RUN apt-get update && apt-get install -y gettext libgettextpo-dev
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/

RUN pip install -r requirements.txt
ADD . /backend/

CMD ["celery", "-A", "taqqoz", "worker", "-B", "-l", "info"]
