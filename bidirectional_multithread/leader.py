import threading
import client
import server
import time
import healthcheck_pb2
import healthcheck_pb2_grpc
import replication_pb2
import replication_pb2_grpc
import grpc
import node_pb2
import node_pb2_grpc
from concurrent import futures

nodesToMonitor=[]
iplist=[]
ipMonitorsWork={}
workDistribution={}
class NodeCommunicationService(node_pb2_grpc.NodeCommunicationServicer):
    def GetNodes(self, request, context):
        nonlocal workDistribution
        reply = node_pb2.GetListOfNodesResponse()
        reply.nodeips.extend(workDistribution[request.nodeip])
        return reply


    def updateNodeMonitorList(self, request, context):
        nonlocal workDistribution
        workDistribution  = request.nodeips
        reply = node_pb2.updateNodeListResponse()
        reply.status="ok"
        return reply

    def proposeLeader(self, request, context):
        pass
    def updateLeader(self, request, context):
        pass



class server:
    def __init__(self,nam):
        self.name=nam
    def serve(self,ip,port):

        print("executing " + self.name)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeCommunicationServicer_to_server(NodeCommunicationService(), server)
        server.add_insecure_port('[::]:{}'.format(port))
        server.start()
        server.wait_for_termination()


class client:
    def __init__(self,nam):
        self.name=nam
    #monitors a remote node
    def remote_call(self,ip,port):
        print("client called "+self.name)
        channel=grpc.insecure_channel('{}:{}'.format(ip,port))
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

    def nodeListUpdate(self,workerip):
        nonlocal workDistribution
        channel=grpc.insecure_channel('{}:50051'.format(workerip))
        req2=node_pb2.nodeList()
        req2.extend([])
        stub=node_pb2_grpc.ReplicationStub(channel)
        req2.nodeip.extend(workDistribution[workerip])
        response2 = stub.updateNodeMonitorList(req2)

        print("updated the node monitor list for remote ip ",response2)
        return response2

class Node:
    def __init__(self,state,ip,nodelist,masternodeip):
        self.state=state
        self.term=0
        self.ip=ip
        self.nodelist=nodelist
        self.masternodeip=masternodeip
        self.s = server("node")
        self.c =client("node")

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
        return list(ipstatus.keys())



    def performLeaderJob(self):
        nonlocal nodesToMonitor
        nonlocal workDistribution
        t1 = threading.Thread(target=self.s.serve, args=("localhost",500051))

        # starting thread 1
        t1.start()
        """
        # wait until thread 1 is completely executed
        t1.join()
        """
        while True:
            nodesToMonitor = self.getNodes(self.masternodeip)


            i=0
            """
            monitor 
            10.0.0.216
            10.0.0.167
            10.0.0.100
            
            """



            workernum=len(self.nodelist)
            i=0
            workdistribution={}
            j=0
            while j<len(nodesToMonitor):
                nodeip=nodesToMonitor[j]
                #all nodes are distributed work
                if self.nodelist[i]!=self.ip:
                    if i==len(self.nodelist)-1:
                        i=0
                    if self.nodelist[i] not in workdistribution:
                        workdistribution[self.nodelist[i]]=[]
                    workdistribution[self.nodelist[i]].append(nodeip)
                    i+=1
                    j+=1
                else:
                    i+=1
            for worker in workdistribution:
                self.c.nodeListUpdate(worker)




    def performMonitorJob(self):
        pass

    def doJob(self):
        if self.state=="leader":
            self.term+=1
            self.performLeaderJob()
        else:
            self.performMonitorJob()

if __name__ == "__main__":
    node =Node("leader","localhost","")