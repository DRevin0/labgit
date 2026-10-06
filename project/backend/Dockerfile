FROM python:3.11-slim

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/

CMD ["python", "/app/app.py"]