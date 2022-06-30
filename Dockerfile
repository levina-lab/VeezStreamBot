FROM nikolaik/python-nodejs:python3.10-nodejs17

WORKDIR /app/
RUN chmod 777 /app

COPY requirements.txt /requirements.txt

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get install -y python3 \
    && apt-get install -y --no-install-recommends python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY start.sh /start.sh

CMD ["python3", "main.py"]
