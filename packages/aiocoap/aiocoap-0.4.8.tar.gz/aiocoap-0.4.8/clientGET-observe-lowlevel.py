#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This demos how the low(er?)-level interface of the context manager
is used to render a request directly into PlumbingRequest."""

import logging
import asyncio

from aiocoap import *
from aiocoap.plumbingrequest import PlumbingRequest

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://localhost/fmp', observe=0)
    plumbing_request = PlumbingRequest(request, logging.getLogger("my_request_log"))

    done = asyncio.get_running_loop().create_future()
    def on_event(e):
        print("Got event", e)
        if e.is_last:
            done.set_result(e.exception)
        return True
    plumbing_request.on_event(on_event)

    interface = await protocol.find_remote_and_interface(request)
    interface.request(plumbing_request)

    await done

if __name__ == "__main__":
    asyncio.run(main())
