FROM python:${PYTHON_RELEASE:-3.11-slim}

# Copy project to workdir
COPY .. /app
WORKDIR /app

RUN apt-get update -y && apt-get install --no-install-recommends -y  \
    libjpeg-dev zlib1g-dev gcc && \
    pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT ["gunicorn", "main:app", "-b", ":9000"]
