import grpc
from concurrent import futures
import time


import replication_pb2
import replication_pb2_grpc
class ReplicationService(replication_pb2_grpc.ReplicationServicer):
    def GetListOfNodes(self, request, context):
        reply = replication_pb2.GetListOfNodesResponse()
        reply.nodeips.extend(["10.0.0.215","10.0.2.3"])
        return reply

    def NodeDownUpdate(self, request, context):
        downip=request.nodeip
        print("Detected that node {} is down".format(downip))
        resp = replication_pb2.StatusResponse()
        resp.status = "ok"
        return resp




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_ReplicationServicer_to_server(ReplicationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
