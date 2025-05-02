FROM python:3.12-slim-bookworm

# `libexpat1-dev`: Needed for `rio-tiler`
# `build-essential`: Needed for `make`
RUN apt update && apt install -y libexpat1-dev build-essential

# Force the output of Python to be unbuffered
ENV PYTHONUNBUFFERED=1
# Avoid Python writing '.pyc' files
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["make", "run"]
