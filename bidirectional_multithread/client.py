# import time
# import grpc
# import healthcheck_pb2
# import healthcheck_pb2_grpc
# #import replication_pb2
# #import replication_pb2_grpc
#
#
# class client:
#     def __init__(self,nam):
#         self.name=nam
#     #monitors a remote node
#     def remote_call(self,ip,port):
#         print("client called "+self.name)
#         channel=grpc.insecure_channel('{}:{}'.format(ip,port))
#         req = healthcheck_pb2.healthCheckRequest()
#         stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
#         print('{}:50052'.format(ip))
#         failed_attempts=0
#         while True:
#             try:
#                 response=stub.healthCheck(req,timeout = 3)
#                 print("successful response ",response)
#                 time.sleep(5)
#                 return "up"
#
#             except Exception as e:
#                 failed_attempts+=1
#                 if failed_attempts!=3:
#                     continue
#                 print("Process failed")
#                 if failed_attempts==3:
#                     print("Failed far too many times. Convery gang leader")
#                     failed_attempts=0
#                     return "down"
#         return "up"
#
#     def sendDownRequest(ip,masterip="localhost"):
#         channel=grpc.insecure_channel('{}:50051'.format(masterip))
#         #req2 = replication_pb2.NodeDownUpdateRequest()
#
#         stub=replication_pb2_grpc.ReplicationStub(channel)
#         req2.nodeip=ip
#         response2 = stub.NodeDownUpdate(req2)
#
#         print("response received from the server is",response2)
#         return response2