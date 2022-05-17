import grpc
from concurrent import futures
import time
import replication_pb2
import replication_pb2_grpc
import healthcheck_pb2_grpc
import healthcheck_pb2
class SentinelMonitoringService(healthcheck_pb2_grpc.SentinelMonitoringServicer):
    def healthCheck(self,request,response):
        print("called")
        reply = healthcheck_pb2.healthCheckReply()
        reply.status="success"
        return reply







class server:
    def __init__(self):
        pass
    def serve(self,ip,port):

        print("executing")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        healthcheck_pb2_grpc.add_SentinelMonitoringServicer_to_server(SentinelMonitoringService(), server)
        server.add_insecure_port('[::]:{}'.format(port))
        server.start()
        server.wait_for_termination()