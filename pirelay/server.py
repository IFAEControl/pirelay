#!/usr/bin/env python3

import time
from concurrent import futures

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
