FROM python:3.8-slim
WORKDIR /app

ADD requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD . /app

CMD ["python", "slackbot.py"]