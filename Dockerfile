FROM python:3.11-slim

RUN apt-get update && apt-get install -y \ 
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]