#!/usr/bin/env python3

import asyncio

from aiocoap import Context, GET, Message, error

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gbulb.gtk

class ObserveApplication:
    def __init__(self):
        super().__init__()
        self.task = None
        self.loop = asyncio.get_event_loop()

    async def setup_network(self):
        self.context = await Context.create_client_context()

    def start_observation(self, uri):
        if self.task:
            self.task.cancel()

        self.task = self.loop.create_task(self.observe(uri))

    async def observe(self, uri):
        self.set_spin(True)

        req = self.context.request(Message(code=GET, uri=uri, observe=0))

        data = (await req.response).payload.decode('utf8')
        self.update_display(data)

        try:
            async for response in req.observation:
                data = response.payload.decode('utf8')
                self.update_display(data)
        finally:
            self.set_spin(False)

class GtkObserveApplication(ObserveApplication):
    async def async_init(self):
        win = Gtk.Window()
        win.connect("delete-event", lambda *args: self.loop.stop())

        h = Gtk.VBox()
        win.add(h)

        urlbox = Gtk.Entry(text='coap+tcp://localhost/time')
        bigbutton = Gtk.Button("Run!", sensitive=False)
        output = Gtk.Label('No data received yet')
        output.set_line_wrap(True)
        spinner = Gtk.Spinner()

        self.update_display = output.set_label
        self.set_spin = lambda active: spinner.start() if active else spinner.stop()

        bigbutton.connect('clicked', lambda *args: self.start_observation(urlbox.props.text))

        h.add(urlbox)
        h.add(bigbutton)
        h.add(output)
        h.add(spinner)

        win.show_all()

        await self.setup_network()

        bigbutton.set_sensitive(True)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(gbulb.gtk.GtkEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(GtkObserveApplication().async_init())
    loop.run_forever()
