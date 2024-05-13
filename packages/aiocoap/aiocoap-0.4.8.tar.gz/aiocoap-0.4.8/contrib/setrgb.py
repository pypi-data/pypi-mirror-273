import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import gbulb
import gbulb.gtk
import asyncio
from aiocoap import *

colors = {
        "black": "000000",
        "red": "ff0000",
        "green": "00ff00",
        "blue": "0000ff",
        "white": "ffffff",
        }

def parse3hex(h):
    return {"R": str(int(h[0:2],16)).encode('ascii'),
        "G": str(int(h[2:4],16)).encode('ascii'),
        "B": str(int(h[4:6],16)).encode('ascii'),
        }

async def set(protocol, uri, r, g, b):
    request = Message(code=PUT, uri=uri)
    request.opt.content_format = 50

    request.payload = ('{"red":"%d","green":"%d","blue":"%d"}'%(r, g, b)).encode('ascii')

    response = await protocol.request(request).response

async def maintask():
    protocol = await Context.create_client_context()

    w = Gtk.Window()
    c = Gtk.ColorChooserWidget()
    c.props.show_editor = True
    c.props.use_alpha = False
    w.add(c)
    w.show_all()
    while True:
        r, g, b = int(c.props.rgba.red*255), int(c.props.rgba.green*255), int(c.props.rgba.blue*255)
        print("set", r, g, b)
        await set(protocol, sys.argv[1] + "/led/all", r, g, b)
        await asyncio.sleep(1)

def main():
    asyncio.set_event_loop_policy(gbulb.gtk.GtkEventLoopPolicy())

    loop = asyncio.get_event_loop()
    GLib.timeout_add(100, lambda: (asyncio.Task(maintask()), 0)[1])
    loop.run_forever()

if __name__ == "__main__":
    main()
