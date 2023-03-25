# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import catalog_handler_pb2 as catalog__handler__pb2


class RequestHandlerStub(object):
    """The Request Handler service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Lookup = channel.unary_unary(
                '/request_handler.RequestHandler/Lookup',
                request_serializer=catalog__handler__pb2.LookupRequest.SerializeToString,
                response_deserializer=catalog__handler__pb2.LookupResponse.FromString,
                )
        self.Trade = channel.unary_unary(
                '/request_handler.RequestHandler/Trade',
                request_serializer=catalog__handler__pb2.TradeRequest.SerializeToString,
                response_deserializer=catalog__handler__pb2.TradeResponse.FromString,
                )


class RequestHandlerServicer(object):
    """The Request Handler service definition.
    """

    def Lookup(self, request, context):
        """Sends Price of the stock if the status is active.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Trade(self, request, context):
        """Executes a Trade for the client and communicates the success of it.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RequestHandlerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Lookup': grpc.unary_unary_rpc_method_handler(
                    servicer.Lookup,
                    request_deserializer=catalog__handler__pb2.LookupRequest.FromString,
                    response_serializer=catalog__handler__pb2.LookupResponse.SerializeToString,
            ),
            'Trade': grpc.unary_unary_rpc_method_handler(
                    servicer.Trade,
                    request_deserializer=catalog__handler__pb2.TradeRequest.FromString,
                    response_serializer=catalog__handler__pb2.TradeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'request_handler.RequestHandler', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RequestHandler(object):
    """The Request Handler service definition.
    """

    @staticmethod
    def Lookup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/request_handler.RequestHandler/Lookup',
            catalog__handler__pb2.LookupRequest.SerializeToString,
            catalog__handler__pb2.LookupResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Trade(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/request_handler.RequestHandler/Trade',
            catalog__handler__pb2.TradeRequest.SerializeToString,
            catalog__handler__pb2.TradeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
