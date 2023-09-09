FROM python:3.10-alpine3.18 AS runtime

COPY src/normalize.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "normalize.py"]