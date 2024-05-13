#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This is a usage example of aiocoap that demonstrates how to implement a
simple client. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

import logging
import asyncio

from aiocoap import *

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

async def main():
    protocol = await Context.create_client_context()

    protocol.client_credentials.load_from_dict({"coaps://poseidon-sid.amsuess.com/*": {"dtls": {"psk": b"secretPSK", "client-identity": b"client_Identity"}}})

    polls = asyncio.create_task(poll(protocol))

    while True:
        await asyncio.sleep(10)

    request = Message(code=GET, uri='coaps://poseidon-sid.amsuess.com/time', observe=0)

    pr = protocol.request(request)

    r = await pr.response
    print("First response: %s\n%r"%(r, r.payload))

    try:
        async for r in pr.observation:
            print("Next result: %s\n%r"%(r, r.payload))
    except Exception as e:
        print("Observation terminated:", e)

async def poll(ctx):
    try:
        while True:
            request = Message(code=GET, uri='coaps://poseidon-sid.amsuess.com/.well-known/core')
            r = ctx.request(request)
            response = await r.response
            r.app_response = None
            print(response)
            del request
            del response
            await asyncio.sleep(3)
    except Exception as e:
        print("Surprise, it didn't work:", e)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
