FROM nikolaik/python-nodejs:python3.10-nodejs17

WORKDIR /app/
RUN chmod 777 /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get install -y python3 \
    && apt-get install -y --no-install-recommends python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

CMD ["python3", "main.py"]
