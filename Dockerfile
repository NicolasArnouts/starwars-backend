FROM python:3.12-slim

# Ensures Docker does not buffer our console output
ENV PYTHONUNBUFFERED 1 

# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE ${APP_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "${APP_HOST}:${APP_PORT}"]
