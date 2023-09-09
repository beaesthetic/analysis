FROM python:3.10-alpine3.18 AS runtime

RUN apk update
RUN apk --no-cache add musl-dev linux-headers g++

COPY src/normalize.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "normalize.py"]