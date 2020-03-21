# pull python image
FROM amancevice/pandas:1.0.1-alpine

# set working directory
WORKDIR /usr/src/madrid_central

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip3 install -r requirements.txt
