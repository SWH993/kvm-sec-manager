FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
RUN apt-get update && apt insall -y --no-install-recommends \
    python3-libvirt \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY manager.py ./

ENTRYPOINT ["python3", "manager.py"]