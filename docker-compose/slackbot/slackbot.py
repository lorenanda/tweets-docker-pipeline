import time 
import slack
from sqlalchemy import create_engine
import config

#client = slack.WebClient(token=)

engine = config.PG_ENGINE
webhook_url = config.WEBHOOK_SLACK


while True:
    logging.critical("\n\nPositive tweet:\n")
    query = pg.execute("SELECT text FROM tweets ORDER BY sentiment DESC LIMIT 1")
    msg = str(list(query))
    logging.critical(msg + "\n")
    output = f'NEW TWEET! {user} just tweeted: {msg} \nSentiment score: {blob_score}'
    data = {'text':output}
    requests.post(url=webhook_url, json=data)

    time.sleep(30)