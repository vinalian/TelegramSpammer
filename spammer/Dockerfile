FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-pip \
    supervisor \
    && apt-get clean

WORKDIR /spammer

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY supervisord.conf /etc/supervisor/supervisord.conf

CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
