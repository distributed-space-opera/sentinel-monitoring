import time
import grpc
import healthcheck_pb2
import healthcheck_pb2_grpc
import replication_pb2
import replication_pb2_grpc



def getNodes(ipstatus={},masternodeip='localhost'):
    #get new nodes from master
    channel=grpc.insecure_channel('{}:50051'.format(masternodeip))
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

    channel=grpc.insecure_channel('{}:50052'.format(ip))
    req = healthcheck_pb2.healthCheckRequest()
    stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
    print('{}:50052'.format(ip))
    failed_attempts=0
    while True:
        try:
            response=stub.healthCheck(req,timeout = 3)
            print("successful response ",response)
            time.sleep(5)
            return "up"

        except Exception as e:
            failed_attempts+=1
            if failed_attempts!=3:
                continue
            print("Process failed")
            if failed_attempts==3:
                print("Failed far too many times. Convery gang leader")
                failed_attempts=0
                return "down"
    return "up"

def sendDownRequest(ip,masterip="localhost"):
    channel=grpc.insecure_channel('{}:50051'.format(masterip))
    req2 = replication_pb2.NodeDownUpdateRequest()

    stub=replication_pb2_grpc.ReplicationStub(channel)
    req2.nodeip=ip
    response2 = stub.NodeDownUpdate(req2)

    print("response received from the server is",response2)
    return response2


if __name__=='__main__':
    iplist={}
    while True:
        try:
            iplist=getNodes(iplist)
            print(iplist)
            for i in iplist:
                print(i)
                iplist[i]=getStatus(i)
                if iplist[i]=="down":
                    sendDownRequest(i)

                time.sleep(2)

            print(iplist)
        except Exception as e:
            #print(e)
            pass


#print(response2)
