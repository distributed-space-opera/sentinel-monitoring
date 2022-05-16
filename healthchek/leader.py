import time

import grpc

import healthcheck_pb2
import healthcheck_pb2_grpc

import replication_pb2
import replication_pb2_grpc

channel=grpc.insecure_channel('localhost:50051')
req = replication_pb2.GetListOfNodesRequest()
req2 = replication_pb2.NodeDownUpdateRequest()
stub=replication_pb2_grpc.ReplicationStub(channel)

failed_attempts=0
"""
while True:

    try:
        print("successful response ",response)
        time.sleep(5)
    except Exception as e:
        failed_attempts+=1
        print("Process failed")
        if failed_attempts==3:
            print("Failed far too many times. Convery gang leader")
            failed_attempts=0
            break
"""
#response =stub.GetListOfNodes(req,timeout = 3)
req2.nodeip="10.0.0.167"
response2 = stub.NodeDownUpdate(req2)

print(response2)
#print(response2)
