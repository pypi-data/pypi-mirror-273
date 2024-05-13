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

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    i = 0
    first = None
    while True:
        i += 1
        request = Message(code=GET, uri='coap://127.0.0.1/time')

        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
            raise
        else:
            if first is None:
                first = response.payload
            print('%s, Result: %s (since %s)\n%r'%(i, response.code, first, response.payload))

        await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
