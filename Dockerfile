# pull python image
FROM amancevice/pandas:1.0.1

# set working directory
WORKDIR /usr/src/madrid_central

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev musl-dev g++ libfreetype6-dev

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip3 install -r requirements.txt
