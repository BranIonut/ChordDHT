FROM python:3.11

RUN apt-get update && apt-get install -y \
    nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50050

CMD ["python", "main.py"]


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
#CMD ["sh", "-c", "python main.py $NODE_ID"]