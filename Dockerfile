FROM python:3.12-slim-bookworm

# Needed for rio-tiler
RUN apt update && apt install -y libexpat1-dev

# Set environment variables to avoid Python writing .pyc files and to force the output of Python to be unbuffered
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create and set the working directory inside the container
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
