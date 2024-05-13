#!/usr/bin/env python3

import asyncio

from kivy.app import App
from kivy.lang.builder import Builder

from observe_gtk import ObserveApplication

class KivyObserveApplication(App, ObserveApplication):
    def build(self):
        return Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    TextInput:
        id: urlbox
        text: 'coap+tcp://localhost/time'
    Button:
        id: btn
        text: 'Loading...'
    Label:
        id: label
        text: 'No data received yet'
        text_size: self.size
        halign: 'center'
        valign: 'middle'
    ProgressBar:
        id: spin
''')

    async def main(self):
        await self.setup_network()

        self._spinning = False

        self.root.ids.btn.text = 'Run!'

        asyncio.get_event_loop().create_task(self.spin())

        async for _ in self.root.ids.btn.async_bind('on_release'):
            self.start_observation(self.root.ids.urlbox.text)

    async def spin(self):
        while True:
            for x in range(0, 100):
                await asyncio.sleep(0.01)
                if self._spinning:
                    self.root.ids.spin.value = x
                else:
                    self.root.ids.spin.value = 0

    def update_display(self, text):
        self.root.ids.label.text = text

    def set_spin(self, active):
        self._spinning = active

    def on_start(self):
        asyncio.get_event_loop().create_task(self.main())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(KivyObserveApplication().async_run())
