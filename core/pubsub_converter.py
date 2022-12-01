import json

from google.cloud import pubsub_v1
from constans import BUCKET_KEY_GCP
from core.format_converte import ExportMusic
from app import app
# from modelos import db

class PubSubConverter:

    def __init__(self):


        self.json_key = f'{BUCKET_KEY_GCP}/key.json'

    def subscriber_message(self):
        subscriber = pubsub_v1.SubscriberClient.from_service_account_json(self.json_key)
        subscription_path = subscriber.subscription_path("flask-test-366421", "pruebas-flask-sub")

        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            print("message:")
            print(message.data)
            value = json.loads(message.data)
            print(value)
            export = ExportMusic()
            export.export_file(value)
            message.ack()

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        print(f"Listening for messages on {subscription_path}..\n")
        with subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()


