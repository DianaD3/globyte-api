FROM python:3

ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .

EXPOSE 5000

CMD ["python", "server.py"]
