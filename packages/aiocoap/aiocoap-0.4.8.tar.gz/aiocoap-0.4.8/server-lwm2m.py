#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This is a usage example of aiocoap that demonstrates how to implement a
simple server. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

from aiocoap.resourcedirectory.client.register import Registerer

class AnyResource(resource.Resource):
    async def render_get(self, request):
        return aiocoap.Message(payload=b"Hi")

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('.well-known', 'core'),
            resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('1', '0', '1'), AnyResource())

    ctx = await aiocoap.Context.create_server_context(root, bind=('', 56830))

    Registerer(ctx, rd='coap://localhost', registration_parameters={'ep': 'server-lwm2m.py'})

    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
