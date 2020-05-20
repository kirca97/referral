FROM python:3.7

RUN apt update && apt -y upgrade

RUN apt install -y gcc

COPY src /app/src

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["uvicorn", "src.main:app", "--reload", "--dns 8.8.8.8"]

EXPOSE 8000

#docker build -t server_helper_refferal .