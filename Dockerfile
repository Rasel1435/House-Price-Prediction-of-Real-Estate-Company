FROM python:3-slim

EXPOSE 8000
# Hugging Face default port is 7860
EXPOSE 7860

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app
# Copy your trained model folder into the container
COPY artifacts/ /app/artifacts/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
