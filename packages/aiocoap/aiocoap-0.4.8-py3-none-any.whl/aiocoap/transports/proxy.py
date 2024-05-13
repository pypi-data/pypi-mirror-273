# SPDX-FileCopyrightText: Christian Amsüss and the aiocoap contributors
#
# SPDX-License-Identifier: MIT

from collections import namedtuple

from .. import interfaces
from ..message import Message, UndecidedRemote

class ProxyAddress(
        namedtuple("_ProxyAddress", ["transport"]),
        interfaces.EndpointAddress):
    """An opaque (and actually almost information-less) object that merely
    tells that the message is being processed through a particular
    TransportProxy transport."""

    @property
    def blockwise_key(self):
        return self.transport.blockwise_key

class TransportProxy(interfaces.RequestInterface):
    def __init__(self, context, forward_context, proxy_scheme, proxy_netloc, capture_filter=lambda msg: True):
        self._context = context
        self._wire = forward_context
        self._proxy_remote = UndecidedRemote(proxy_scheme, proxy_netloc)
        self._capture_filter = capture_filter

    async def fill_or_recognize_remote(self, message):
        if isinstance(message.remote, ProxyAddress) and message.remote.transport is self:
            # WTF?
            return False

        if self._capture_filter(message):
            message.remote = ProxyAddress(self)
            return True
        return False

    def request(self, request):
        msg = request.request

        wrapped_msg = Message.copy(msg,
                uri_path=[], uri_query=[], uri_host=None, uri_port=None, proxy_scheme=None,
                proxy_uri=msg.get_request_uri(),
                )
        wrapped_msg.remote = self._proxy_remote

        wire_request = self._wire.request(wrapped_msg)
        def done(response):
            try:
                request.add_response(response.result(), is_last=True)
            except Exception as e:
                request.add_exception(e)
        wire_request.response.add_done_callback(done)
