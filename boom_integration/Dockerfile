FROM python:3.12

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY boom_integration/ ./boom_integration/
COPY yolo11n.pt .

CMD ["uvicorn", "boom_integration.main:app", "--host", "0.0.0.0", "--port", "8000"] 