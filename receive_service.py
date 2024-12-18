from google.cloud import pubsub_v1
from google.oauth2 import service_account
from concurrent.futures import TimeoutError


project_id = "civic-automata-435117-h3"
subscription_id = "bus-data-sub"
cred = service_account.Credentials.from_service_account_file(
    "./civic-automata-435117-h3-412a587990c2.json"
)
# Number of seconds the subscriber should listen for messages
timeout = 50.0

subscriber = pubsub_v1.SubscriberClient(credentials=cred)
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(type(message.data.decode("utf-8")))
    # print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.