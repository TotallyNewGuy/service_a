import os
import asyncio
import constants
from datetime import datetime
from aiohttp import ClientSession

from pub_sub_util import publish_message


async def update_arrivals():
    curr_day = datetime.now(constants.TZINFO).weekday()
    day_type = 1
    if curr_day == 5:  # Saturday
        day_type = constants.cta_day_type["Saturday"]
    elif curr_day == 6:  # Sunday
        day_type = constants.cta_day_type["Sunday"] 

    try:
        await update_arrt_headway(day_type)
        return 'Successfully fetched predictions from CTA'
    except Exception as e:
        return f'Failed to update predictions: {e}'


async def update_arrt_headway(day_type: int):
    async with ClientSession() as session:
        requests = [
            _update_through_CTA(session, stop_name, day_type)
            for stop_name in constants.stop_map
        ]
        await asyncio.gather(*requests)


async def _update_through_CTA(session: ClientSession, stop_name: str, day_type: int):
    TRAIN_TRACKER_KEY = os.getenv("TRAIN_TRACKER_KEY")
    TRAIN_BASE_URL = constants.TRAIN_BASE_URL
    ROUTE = constants.ROUTE
    url = (
        TRAIN_BASE_URL
        + f"ttarrivals.aspx?key={TRAIN_TRACKER_KEY}&"
        + f"rt={ROUTE}&"
        + f"stpid={constants.stop_map[stop_name]}"
        + f"&outputType=JSON&showintervals=1"
    )

    async with session.get(url) as resp:
        temp = await resp.json()
        if "eta" not in temp["ctatt"]:
            return None
        respon_json_raw: list[dict] = temp["ctatt"]["eta"]
        tmst = temp['ctatt']['tmst']
        # each stop has one list of records
        await publish_message({
            "respon_json_raw": respon_json_raw,
            "stop_name": stop_name,
            "day_type": day_type,
            "tmst": tmst
        }, os.getenv("TOPIC_ID"))