FROM python:3.11

RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir -p /app/logs && touch /app/logs/app.log && chmod -R 777 /app/logs

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50050

CMD ["python", "main.py"]

#
#FROM python:3.11
#
#RUN apt-get update && apt-get install -y \
#    nmap \
#    && rm -rf /var/lib/apt/lists/*
#
#WORKDIR /app
#
#COPY . .
#
#RUN pip install --no-cache-dir -r requirements.txt
#
#EXPOSE 50050
#
#CMD ["sh", "-c", "python main-docker.py $NODE_ID"]