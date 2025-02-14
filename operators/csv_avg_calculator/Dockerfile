FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY calculate_avg.py .
ENTRYPOINT ["python", "calculate_avg.py"]
