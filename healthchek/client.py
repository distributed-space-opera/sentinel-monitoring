import grpc

import healthcheck_pb2
import healthcheck_pb2_grpc

channel=grpc.insecure_channel('localhost:50051')
req = healthcheck_pb2.healthCheckRequest()
stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
response=stub.healthCheck(req)
print("received reponse",response.status)