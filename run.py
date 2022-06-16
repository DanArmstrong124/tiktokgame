from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *
from bs4 import BeautifulSoup as bs

import os

import re

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(
    unique_id="@danarms_x", **(
        {
            # Whether to process initial data (cached chats, etc.)
            "process_initial_data": True,

            # Connect info (viewers, stream status, etc.)
            "fetch_room_info_on_connect": True,

            # Whether to get extended gift info (Image URLs, etc.)
            "enable_extended_gift_info": True,

            # How frequently to poll Webcast API
            "polling_interval_ms": 1000,

            # Custom Client params
            "client_params": {},

            # Custom request headers
            "headers": {},

            # Custom timeout for Webcast API requests
            "timeout_ms": 1000,

            # Custom Asyncio event loop
            "loop": None,

            # Whether to trust environment variables that provide proxies to be used in aiohttp requests
            "trust_env": False,

            # A ProxyContainer object for proxied requests
            "proxy_container": None,

            # Set the language for Webcast responses (Changes extended_gift's language)
            "lang": "en-US"

        }
    )
)

# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

@client.on("like")
async def on_like(event: LikeEvent):
    print(f"{event.user.nickname} liked the stream!")

@client.on("join")
async def on_join(event: JoinEvent):
    print(f"{event.user.nickname} joined the stream!")

@client.on("gift")
async def on_gift(event: GiftEvent):
    # If it's type 1 and the streak is over
    if event.gift.gift_type == 1:
        if event.gift.repeat_end == 1:
            print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        print(f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\"")

@client.on("follow")
async def on_follow(event: FollowEvent):
    print(f"{event.user.nickname} followed the streamer!")

@client.on("share")
async def on_share(event: ShareEvent):
    print(f"{event.user.nickname} shared the streamer!")

# Notice no decorator?
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")


# Define handling an event via "callback"
client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()


base=os.path.dirname(os.path.abspath(__file__))
html=open(os.path.join(base, ‘index’))
soup=bs(html, ‘html.parser’)