FROM python:3

WORKDIR /usr/src/app

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin libgdal-dev

COPY requirements.txt ./

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal

ENV C_INCLUDE_PATH=/usr/include/gdal

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./rando.py" ]
