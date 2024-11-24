FROM python:3.13

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "fastapi", "run", "--port", "8000" ]