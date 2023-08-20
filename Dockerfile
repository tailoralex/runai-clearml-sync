FROM python:3.9-alpine
RUN apk add linux-headers build-base python3-dev libressl-dev
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
