FROM python:3.12.6-slim

ENV PYTHONE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./core /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]