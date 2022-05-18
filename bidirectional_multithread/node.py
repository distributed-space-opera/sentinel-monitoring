import grpc
from concurrent import futures
import time

import healthcheck_pb2_grpc
import healthcheck_pb2

class SentinelMonitoringService(healthcheck_pb2_grpc.SentinelMonitoringServicer):
    def healthCheck(self,request,response):
        reply = healthcheck_pb2.healthCheckReply()
        reply.status="success"
        return reply





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    healthcheck_pb2_grpc.add_SentinelMonitoringServicer_to_server(SentinelMonitoringService(), server)
    server.add_insecure_port('[::]:50071')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
