####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY saudi_tourism saudi_tourism

CMD uvicorn saudi_tourism.api.fast:app --host 0.0.0.0 --port $PORT
