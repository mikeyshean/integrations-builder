FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /django

ARG DEV_BUILD=true
COPY requirements*.txt /tmp/
RUN if [ "$DEV_BUILD" = "true" ]; then \
        pip3 install -r /tmp/requirements-dev.txt --src /src; \
    else \
        pip3 install -r /tmp/requirements.txt --src /src; \
    fi \
    && rm /tmp/requirements*.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]