# Imagem base oficial Python 3.11 slim (mais leve)
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Evitar criação de arquivos .pyc e buffer no stdout/stderr (útil para logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualizar pacotes e instalar dependências do sistema (curl e gcc podem ser necessários)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências para cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte para dentro do container
COPY . .

# Expõe a porta onde o Flask irá rodar
EXPOSE 5000

# Comando para iniciar o servidor Gunicorn com 4 workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
