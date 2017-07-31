import grpc


from .protos import pirelay_pb2
from .protos import pirelay_pb2_grpc


class Client(object):
    def __init__(self, ip):
        channel = grpc.insecure_channel('{}:50051'.format(ip))
        self.stub = pirelay_pb2_grpc.PiRelayStub(channel)

    def enable(self, channel):
        response = self.stub.Enable(pirelay_pb2.PiRelayChannel(channel=channel))

        if response.type == pirelay_pb2.Error:
            raise Exception(response.message)

    def disable(self, channel):
        response = self.stub.Disable(pirelay_pb2.PiRelayChannel(channel=channel))

        if response.type == pirelay_pb2.Error:
            raise Exception(response.message)


