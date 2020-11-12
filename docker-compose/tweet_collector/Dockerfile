FROM python:3.8-slim

WORKDIR /app

#ADD requirements.txt /app
#ADD tweet_streamer.py /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python", "tweet_streamer.py"]