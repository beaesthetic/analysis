FROM python:3.10-alpine3.18 AS runtime

RUN apk update
RUN apk --no-cache add musl-dev linux-headers g++

COPY src src
COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR src/

ENTRYPOINT ["python", "normalize.py"]