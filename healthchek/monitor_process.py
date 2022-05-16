import time

import grpc

import healthcheck_pb2
import healthcheck_pb2_grpc

import replication_pb2
import replication_pb2_grpc

req2 = replication_pb2.NodeDownUpdateRequest()

failed_attempts=0
#ipstore={"10.0.0.203":"up","10.0.0.203":"down","10.0.0.203":"up",}
ipstatus={}


def getNodes(ipstatus={}):
    #get new nodes from master
    channel=grpc.insecure_channel('localhost:50051')
    stub=replication_pb2_grpc.ReplicationStub(channel)
    req = replication_pb2.GetListOfNodesRequest()
    response =stub.GetListOfNodes(req,timeout = 3)
    response=str(response).split("\n")[:-1]
    for i in response:
        ip = i.split(":")[1].strip()[1:-1]
        if ip not in ipstatus:
            ipstatus[ip]="up"
    print(ipstatus)
    return ipstatus



def getStatus(ip):
    channel=grpc.insecure_channel('{}:50051'.format(ip))
    req = healthcheck_pb2.healthCheckRequest()
    stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
    failed_attempts=0

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
            return "down"
    time.sleep(5)
    return "up"

def sendDownRequest(ip):
    channel=grpc.insecure_channel('{}:50051'.format(ip))

    stub=replication_pb2_grpc.ReplicationStub(channel)
    req2.nodeip=ip
    response2 = stub.NodeDownUpdate(req2)

    print(response2)
    return response2



iplist={}
while True:
    try:
        iplist=getNodes(iplist)
        for i in iplist:
            iplist[i]=getStatus(iplist[i])
            if iplist[i]=="down":
                sendDownRequest(iplist[i])

            time.sleep(2)


    except Exception as e:
        print(e)


#print(response2)
