FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements/production.txt .
RUN pip install -r production.txt
COPY . .
