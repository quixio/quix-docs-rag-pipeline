from flask import Flask, request, jsonify
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
import datetime
import json

from flask import Flask, request, Response
from waitress import serve

from setup_logging import get_logger

from quixstreams.platforms.quix import QuixKafkaConfigsBuilder
from quixstreams.kafka import Producer

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

cfg_builder = QuixKafkaConfigsBuilder()
cfgs, topics, _ = cfg_builder.get_confluent_client_configs([os.environ["output"]])
producer = Producer(cfgs.pop("bootstrap.servers"), extra_config=cfgs)

logger = get_logger()

app = Flask(__name__)
client = WebClient(token=os.environ['slack_token'])

@app.route('/slack/events', methods=['POST'])
def slack_events():
    json_data = request.json
    print(json_data)
    # Check for Slack's challenge response
    if "challenge" in json_data:
        return jsonify({'challenge': json_data['challenge']})

    channel_id = message['event']['channel']

    producer.produce(topics[0], json.dumps(data), channel_id)

    return jsonify({'status': 'ok'}), 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=80)
