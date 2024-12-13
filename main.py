import os
import asyncio
from quart import Quart
from quart_cors import cors
from dotenv import load_dotenv

from poll_from_CTA import update_arrivals
from topic_blueprint import topic_blueprint
from pub_sub_util import init_pub_sub_client



def create_app():
    load_dotenv()
    # The main app
    app = Quart(__name__)
    # enable CORS
    app = cors(app, allow_origin="*")
    app.register_blueprint(topic_blueprint)
    return app


app = create_app()


async def poll_and_publish():
    while True:
        await update_arrivals()
        await asyncio.sleep(60)


@app.before_serving
async def start_background_task():
    init_pub_sub_client()
    # Start the background task
    asyncio.create_task(poll_and_publish())


@app.route("/")
async def hello_world():
    return "<p>Hello World from Service A!</p>"


if __name__ == "__main__":
    # Run the Quart(Flask) app when run this Python file
    DEBUG = os.getenv("DEBUG").lower() == 'true'
    port = int(os.getenv("PORT", 8080))
    print(f"listening post: {port}")
    app.run(debug=DEBUG, port=port, host="0.0.0.0")