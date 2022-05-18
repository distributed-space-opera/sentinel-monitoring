import threading
import client
import server
import time
import healthcheck_pb2
import healthcheck_pb2_grpc
import replication_pb2
import replication_pb2_grpc
import grpc
import node_pb2
import node_pb2_grpc
from concurrent import futures
channel=grpc.insecure_channel('localhost:50062')
req = node_pb2.nodeList()

stub=node_pb2_grpc.NodeCommunicationStub(channel)
req.nodeips.extend(["localhost:50071"])
response=stub.updateNodeMonitorList(req)
print(response)