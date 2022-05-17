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
#ipstore={"10.0.0.203":"up","10.0.0.203":"down","10.0.0.203":"up",}
ipstatus={}
response =stub.GetListOfNodes(req,timeout = 3)

response=str(response).split("\n")[:-1]
for i in response:
    ip = i.split(":")[1].strip()[1:-1]
    ipstatus[ip]="up"
print(ipstatus)
client_ips={"10.0.0.167":{"ipm":["10.0.0.203"],"status":"up"}}


while True:

    try:
        i=0
        while i<len(client_ips):

            client=client_ips.keys()[i]
            if client_ips[client]["status"]=="up":
                channel=grpc.insecure_channel('{}:50051'.format(client))
                stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
                req=healthcheck_pb2.healthCheckRequest()
                try :
                    resp  = stub.clientAlive(req,timeout=3)
                    print("client is alive ",resp)
                    time.sleep(3)
                except Exception as e1:
                    failed_attempts+=1
                    if failed_attempts!=3:
                        continue
                    print("Client failed")
                    if failed_attempts==3:
                        print("Failed far too many times. Convey gang leader")
                        failed_attempts=0
                        client_ips[client]["status"]="down"
            i+=1


        time.sleep(10)
        print('refetching the new list of resources')
        channel=grpc.insecure_channel('localhost:50051')
        req = replication_pb2.GetListOfNodesRequest()
        stub=replication_pb2_grpc.ReplicationStub(channel)
        response =stub.GetListOfNodes(req,timeout = 3)
        response=str(response).split("\n")[:-1]
        for newip in response:
            newip = newip.split(":")[1].strip()[1:-1]
            if newip not in ipstatus:
                ipstatus[newip]="up"



    except Exception as e:
        print(e)


req2.nodeip="10.0.0.167"
response2 = stub.NodeDownUpdate(req2)

print(response2)
#print(response2)
