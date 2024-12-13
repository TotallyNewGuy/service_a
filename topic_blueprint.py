import os
from google.cloud import pubsub_v1
from quart import Blueprint, g, request
from pub_sub_util import get_publisher, get_subscriber, publish_message

# create a blueprint for url prefix
topic_blueprint = Blueprint('topic_api', __name__, url_prefix='/topic')


@topic_blueprint.route("/list")
async def list_topics():
    project_path = f"projects/{os.getenv('PROJECT_ID')}"
    topics = []
    for topic in get_publisher().list_topics(request={"project": project_path}):
        string_list = topic.name.split("/")
        topics.append(string_list[-1])
    return {"topic_list": topics}


@topic_blueprint.route("/create/<string:topic>")
async def create_topic(topic):
    topic_path = get_publisher().topic_path(os.getenv("PROJECT_ID"), topic)
    topic_full_name = get_publisher().create_topic(request={"name": topic_path})
    return f"Created topic {topic_full_name}"


@topic_blueprint.route("delete/<string:topic>")
async def delete_topic(topic):
    topic_path = get_publisher().topic_path(os.getenv("PROJECT_ID"), topic)
    res = get_publisher().delete_topic(request={"topic": topic_path})
    return f"Delete topic topic res: {'successful' if res is None else 'something wrong'}"


@topic_blueprint.route("subscribe/<string:topic>")
async def subscribe_topic(topic):
    subscription_path = get_subscriber().subscription_path(os.getenv("PROJECT_ID"), topic)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(message.data.decode("utf-8"))
        message.ack()
    streaming_pull_future = get_subscriber().subscribe(subscription_path, callback=callback)
    g.pubsub_client = streaming_pull_future


@topic_blueprint.route("publish/<string:topic>", methods=['POST'])
async def publish_to_topic(topic):
    content_type = request.headers.get('content-type')
    if (content_type == 'application/json'):
        request_json = await request.get_json()
        res = await publish_message(request_json, topic)
    return res