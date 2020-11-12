FROM python:3.8-slim
#download debian linux & python
WORKDIR /app
# mkdir app && cd app

ADD requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "etl.py"]