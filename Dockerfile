FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code

COPY . .
COPY entrypoint2.sh .

EXPOSE 8000

RUN chmod -R 777 /code

CMD ["./entrypoint2.sh"]