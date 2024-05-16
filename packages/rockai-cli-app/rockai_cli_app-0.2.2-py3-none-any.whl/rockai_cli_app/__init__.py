from typing import Iterator, Dict, Optional, Any, List, AsyncIterator
import json
import requests
from sseclient import SSEClient
import time
import httpx
from httpx_sse import connect_sse
import logging
import asyncio
from aiosseclient import aiosseclient
from aiohttp_sse_client import client as sse_client
import os


logging.basicConfig(level=logging.DEBUG)

# testing
# predict_url = "http://localhost:8000/v1/predictions"
# get_url = "http://localhost:8000/v1/predictions/{}"
# token = os.environ.get('ROCK_API_TOKEN')
# logging.info("Token: {}".format(token))
# cancel_url = "http://localhost:8000/v1/predictions/{}/cancel"

# production
predict_url = "https://jd5mv2ryxs.ap-northeast-1.awsapprunner.com/v1/predictions"
get_url = "https://jd5mv2ryxs.ap-northeast-1.awsapprunner.com/v1/predictions/{}"
token = os.environ.get('ROCK_API_TOKEN')
logging.info("Token: {}".format(token))
cancel_url = "https://jd5mv2ryxs.ap-northeast-1.awsapprunner.com/{}/cancel"




def stream(version: str, input: Optional[Dict[str, Any]] = None) -> Iterator:
    url = predict_url

    payload = {"version": version, "input": input, "stream": True}

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    response = requests.post(url=url, headers=headers, json=payload)
    response.raise_for_status()
    create_result = response.json()
    if (
        response.status_code == 200
        or response.status_code == 201
        and "stream" in create_result["data"]["urls"]
    ):
        headers["Accept"] = "text/event-stream"
        headers["Cache-Control"] = "no-store"

        with httpx.Client() as client:
            with connect_sse(
                client, create_result["data"]["urls"]["stream"]
            ) as event_source:
                try:
                    for sse in event_source.iter_sse():
                        yield sse.data
                except Exception as e:
                    logging.error(str(e))


def run(
    version: str,
    input: Optional[Dict[str, Any]] = None,
    webhook: Optional[str] = None,
    webhook_events_filter: Optional[List[str]] = None,
) -> Any:
    url = predict_url

    payload = {"version": version, "input": input}
    if webhook is not None:
        payload["webhook"] = webhook
    if webhook_events_filter is not None:
        payload["webhook_events_filter"] = webhook_events_filter

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    response = requests.post(url=url, headers=headers, json=payload)
    response.raise_for_status()
    create_result = response.json()
    if response.status_code == 200 or response.status_code == 201:
        while True:
            get_resp = requests.get(
                url=get_url.format(create_result["data"]["id"]), headers=headers
            )
            get_resp.raise_for_status()
            get_result = get_resp.json()
            if (
                get_result["data"]["status"] == "processing"
                or get_result["data"]["status"] == "starting"
            ):
                time.sleep(1)
                continue
            else:
                return get_result


async def stream_async(version: str, input: Optional[Dict[str, Any]] = None):
    url = predict_url

    payload = {"version": version, "input": input, "stream": True}

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        create_result = response.json()
        if "stream" in create_result["data"]["urls"]:

            logging.info(create_result["data"]["urls"])
            async with sse_client.EventSource(
                create_result["data"]["urls"]["stream"]
            ) as event_source:

                async for event in event_source:
                    yield event.data
                    if event.type == "done" and event.message == "done":
                        return


async def run_async(
    version: str,
    input: Optional[Dict[str, Any]] = None,
    webhook: Optional[str] = None,
    webhook_events_filter: Optional[List[str]] = None,
):
    url = predict_url

    payload = {"version": version, "input": input}
    if webhook is not None:
        payload["webhook"] = webhook
    if webhook_events_filter is not None:
        payload["webhook_events_filter"] = webhook_events_filter

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        create_result = response.json()
        while True:
            get_resp = await client.get(
                url=get_url.format(create_result["data"]["id"]), headers=headers
            )
            get_result = get_resp.json()
            if (
                get_result["data"]["status"] == "processing"
                or get_result["data"]["status"] == "starting"
            ):
                await asyncio.sleep(1)
                continue
            else:
                return get_result


# it = stream("5fe0a3d7ac2852264a25279d1dfb798acbc4d49711d126646594e212cb821749",{
#       "top_k": 50,
#       "top_p": 0.9,
#       "prompt": "Can you write me a poem about steamed hams?",
#       "max_new_tokens": 500
# 	}
#     )


# for item in it:
#     print(item)

# run("f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",input={
#             "top_p": 1,
#             "prompt": "Plan a day of sightseeing for me in San Francisco. ",
#             "temperature": 0.75,
#             "system_prompt": "You are an old-timey gold prospector who came to San Francisco for the gold rush and then was teleported to the present day. Despite being from 1849, you have great knowledge of present-day San Francisco and its attractions. You are helpful, polite, and prone to rambling. ",
#             "max_new_tokens": 800,
#             "repetition_penalty": 1
#         })


async def main():
    async for i in stream_async(
        "f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",
        input={
            "top_p": 1,
            "prompt": "Plan a day of sightseeing for me in San Francisco. ",
            "temperature": 0.75,
            "system_prompt": "You are an old-timey gold prospector who came to San Francisco for the gold rush and then was teleported to the present day. Despite being from 1849, you have great knowledge of present-day San Francisco and its attractions. You are helpful, polite, and prone to rambling. ",
            "max_new_tokens": 800,
            "repetition_penalty": 1,
        },
    ):
        print(i)
    # result = await run_async("f1d50bb24186c52daae319ca8366e53debdaa9e0ae7ff976e918df752732ccc4",input={
    #         "top_p": 1,
    #         "prompt": "Plan a day of sightseeing for me in San Francisco. ",
    #         "temperature": 0.75,
    #         "system_prompt": "You are an old-timey gold prospector who came to San Francisco for the gold rush and then was teleported to the present day. Despite being from 1849, you have great knowledge of present-day San Francisco and its attractions. You are helpful, polite, and prone to rambling. ",
    #         "max_new_tokens": 800,
    #         "repetition_penalty": 1
    #     })
    # print(result)


asyncio.run(main())
