FROM python:3.9-slim as base

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage preprocessing
FROM base as preprocessing
COPY preprocessing.py .
COPY train.csv /app/data/
COPY test.csv /app/data/
VOLUME /app/data
VOLUME /app/output
CMD ["python", "preprocessing.py"]

# Stage training
FROM base as training
COPY train.py .
VOLUME /app/data
VOLUME /app/models
CMD ["python", "train.py"]

# Stage evaluation
FROM base as evaluation
COPY evaluate.py .
VOLUME /app/data
VOLUME /app/models
VOLUME /app/metrics
CMD ["python", "evaluate.py"]