# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time

import grpc

from .protos import pirelay_pb2
from .protos import pirelay_pb2_grpc

from .relay import RelaysArray

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

PINS = [21]


class PiRelayServer(pirelay_pb2_grpc.PiRelayServicer):

    def __init__(self, bcm_pins=[]):
        self._relays = RelaysArray(bcm_pins=bcm_pins)

    def Enable(self, request, context):

        try:
            self._relays.enable(request.channel)
        except Exception as ex:
            return pirelay_pb2.PiRelaysAnswer(type=pirelay_pb2.Error,
                                              message=str(ex))
        else:
            return pirelay_pb2.PiRelaysAnswer(type=pirelay_pb2.Ok,
                                              message="")

    def Disable(self, request, context):

        try:
            self._relays.disable(request.channel)
        except Exception as ex:
            return pirelay_pb2.PiRelaysAnswer(type=pirelay_pb2.Error,
                                              message=str(ex))
        else:
            return pirelay_pb2.PiRelaysAnswer(type=pirelay_pb2.Ok,
                                              message="")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pirelay_pb2_grpc.add_PiRelayServicer_to_server(PiRelayServer(PINS), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
