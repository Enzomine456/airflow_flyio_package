FROM python:3.11-slim

# Atualiza e instala dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta 5000 (opcional, Fly.io pode detectar automaticamente)
EXPOSE 5000

# Comando para iniciar a aplicação com gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
