FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y libmagic1
RUN mkdir /images
RUN mkdir /app

RUN apt-get update
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

EXPOSE 8282

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8282 --workers 4"]
