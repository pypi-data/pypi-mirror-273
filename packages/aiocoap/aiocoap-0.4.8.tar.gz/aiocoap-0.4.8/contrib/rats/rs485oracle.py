#!/usr/bin/env python3

import asyncio
import aiocoap.resource as resource
import aiocoap

class Oracle(resource.Resource):
    async def render_get(self, request):
        result = rs485.ask()
        return aiocoap.Message(payload=result)

    async def render_put(self, request):
        print("I'm accepting the put")
        return aiocoap.Message()

def main():
    root = resource.Site()
    root.add_resource(('oracle',), Oracle())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
