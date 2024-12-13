import os, json
from google.cloud import pubsub_v1
from google.oauth2 import service_account

publisher, subscriber = None, None

def init_pub_sub_client():
    global publisher, subscriber

    credentials_json = os.getenv("GCP_CRED")
    if credentials_json is None:
        raise ValueError("Didn't set GCP_CRED")
    credentials_info = json.loads(credentials_json)
    cred = service_account.Credentials.from_service_account_info(credentials_info)
    publisher = pubsub_v1.PublisherClient(credentials=cred)
    subscriber = pubsub_v1.SubscriberClient(credentials=cred)
    return publisher, subscriber


def get_publisher():
    return publisher


async def publish_message(json_data, topic):
    json_str = json.dumps(json_data)
    # Data must be a bytestring
    data = json_str.encode("utf-8")
    topic_path = get_publisher().topic_path(os.getenv("PROJECT_ID"), topic)
    # When you publish a message, the client returns a future.
    future = get_publisher().publish(topic_path, data)
    # print(f"Published {json_data} to topic {topic}, message_id: {future.result()}")


def get_subscriber():
    return subscriber