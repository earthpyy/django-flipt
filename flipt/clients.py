"""Flipt gRPC client"""
import grpc
from flipt_pb2_grpc import FliptStub
from django.conf import settings


channel = grpc.insecure_channel(settings.FLIPT_GRPC_HOST)
client = FliptStub(channel=channel)
