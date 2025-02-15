FROM python:3.9

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERD 1

#RUN pip install --upgrade pip

COPY requirements.txt /usr/src/app/requirements.txt
#COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN pip install -r requirements.txt

COPY . /usr/src/app/