FROM python:3.10-alpine3.18 AS runtime

RUN apk update
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev

COPY src/normalize.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "normalize.py"]