# Imagem base oficial Python 3.11 slim (menor e segura)
FROM python:3.11-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Evitar criar arquivos __pycache__ e bytecode no container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualizar pacotes e instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências Python com cache desligado para imagem leve
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação para o container
COPY . .

# Definir variáveis de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expõe a porta que o Flask vai usar
EXPOSE 5000

# Usar Gunicorn para rodar o app Flask em produção com múltiplos workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
