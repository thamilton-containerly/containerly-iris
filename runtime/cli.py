import base64
import click
import grpc
import json
import logging
from concurrent import futures
from google.protobuf import json_format
from grpc_reflection.v1alpha import reflection
from runtime import app
from runtime import containerly_pb2_grpc, containerly_pb2


class Runtime(containerly_pb2_grpc.RuntimeServicer):

    def Service(self, request, context):
        runtime_input_dict = json_format.MessageToDict(request)
        message = runtime_input_dict["message"]
        bytes_decoded_message = base64.b64decode(message)
        string_decoded_message = bytes_decoded_message.decode()
        json_decoded_message = json.loads(string_decoded_message)
        response = app.run_service(json_decoded_message)
        runtime_output_response = containerly_pb2.Response()
        runtime_output_response.message = json.dumps(response).encode('utf-8')
        return runtime_output_response


@click.group()
def cli():
    """Top-level runtime command entry point"""


@cli.command()
def serve():
    logging.basicConfig()
    server = grpc.server(
        thread_pool=futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[]
    )
    containerly_pb2_grpc.add_RuntimeServicer_to_server(
        Runtime(), server
    )
    SERVICE_NAMES = (
        containerly_pb2.DESCRIPTOR.services_by_name['Runtime'].full_name,
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def service_request(channel, message_bytes):
    stub = containerly_pb2_grpc.RuntimeStub(channel)
    return stub.Service(
        containerly_pb2.Request(
            message=message_bytes
        )
    )


@cli.command()
@click.option("--host", required=True, type=str, default="localhost", help="GRPC host")
@click.option("--port", required=True, type=str, default="50051", help="GRPC port")
@click.option("--payload", required=True, type=str, default='{"message": "eyJoZWxsbyI6ICJuaW5qYSJ9"}',
              help="GRPC message")
@click.option("--insecure", required=True, type=bool, default=True, help="security")
def client(host, port, payload, insecure):
    json_payload = json.loads(payload)
    json_str_payload = json.dumps(json_payload)
    message_bytes = json_str_payload.encode("utf-8")
    credentials = grpc.ssl_channel_credentials()
    # TODO - Fix secure/insecure logic
    if insecure:
        with grpc.insecure_channel(host + ":" + port) as channel:
            response = service_request(channel, message_bytes)
            print(response)
    else:
        with grpc.secure_channel(host + ":" + port, credentials) as channel:
            response = service_request(channel, message_bytes)
            print(response)
