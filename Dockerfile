FROM python:3.11-slim-bookworm
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY entrypoint.sh .
RUN ["chmod", "+x", "entrypoint.sh"]

CMD ["sh","entrypoint.sh","run"]
