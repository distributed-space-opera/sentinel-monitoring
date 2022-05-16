import time

import grpc

import healthcheck_pb2
import healthcheck_pb2_grpc


channel=grpc.insecure_channel('10.0.0.215:50051')
req = healthcheck_pb2.healthCheckRequest()
stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
failed_attempts=0

class SentinelMonitoringService(healthcheck_pb2_grpc.SentinelMonitoringServicer):
    def healthCheck(self,request,response):
        reply = healthcheck_pb2.healthCheckReply()
        reply.status="success"
        return reply

    def clientAlive(self, request, context):
        reply = healthcheck_pb2.healthCheckReply()
        reply.status="up"
        return reply


while True:

    try:
        response=stub.healthCheck(req,timeout = 3)
        print("successful response ",response.status)
        time.sleep(5)
    except Exception as e:
        failed_attempts+=1
        print("Process failed")
        if failed_attempts==3:
            print("Failed far too many times. Convery gang leader")
            failed_attempts=0
            break