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
        global workDistribution
        reply = node_pb2.GetListOfNodesResponse()
        reply.nodeips.extend(workDistribution[request.nodeip])
        return reply


    def updateNodeMonitorList(self, request, context):
        global workDistribution
        print("update Node: -->", request.nodeips)
        workDistribution = request.nodeips
        print("workDistribution: ", workDistribution)
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
    def serve(self,ipandport):
        ip = ipandport.split(':')[0]
        port = ipandport.split(':')[1]

        print("executing " + self.name)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeCommunicationServicer_to_server(NodeCommunicationService(), server)
        server.add_insecure_port('{}:{}'.format(ip,port))
        server.start()
        server.wait_for_termination()

    # def nodeListUpdate(self, workerip,nodeList):
    #     channel = grpc.insecure_channel('{}'.format(workerip))
    #     req2 = node_pb2.nodeList()
    #     # req2.extend([])
    #     print("Workerip: ", workerip)
    #     stub = node_pb2_grpc.NodeCommunicationStub(channel)
    #     # req2.nodeips.append(workDistribution[workerip])
    #
    #     req2.nodeips.extend(workDistribution[workerip])
    #     print("Req2: ", req2)
    #     response2 = stub.updateNodeMonitorList(req2)
    #
    #     print("updated the node monitor list for remote ip ", response2)
    #     return response2


class client:
    def __init__(self,nam):
        self.name=nam
    #monitors a remote node
    def remote_call(self,ipandport):
        ip=ipandport.split(':')[0]
        port = ipandport.split(':')[1]
        print("client called "+self.name)
        print("ipandport: ", ipandport)
        channel=grpc.insecure_channel('{}:{}'.format(ip,port))
        req = healthcheck_pb2.healthCheckRequest()
        stub=healthcheck_pb2_grpc.SentinelMonitoringStub(channel)
        # print('{}:{}'.format(ip, port))
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

    def sendDownRequest(ip, masterip="localhost", masterport=50051):
        channel=grpc.insecure_channel('{}:{}'.format(masterip, masterport))
        req2 = replication_pb2.NodeDownUpdateRequest()

        stub=replication_pb2_grpc.ReplicationStub(channel)
        req2.nodeip=ip
        response2 = stub.NodeDownUpdate(req2)

        print("response received from the server is",response2)
        return response2

class Node:
    def __init__(self,state,ip,nodelist,masternodeip):
        self.state=state
        self.term=0
        self.ip=ip
        self.nodelist=nodelist
        self.masternodeip=masternodeip
        # self.masternodeport = masternodeport
        self.s = server("node")
        self.c =client("node")
        self.doJob()
        t1 = threading.Thread(target=self.s.serve, args=(self.ip))
        t1.start()

    def nodeListUpdate(self, workerip):
        global workDistribution
        print("---------->",workDistribution)
        print("workerip------->",workerip)
        channel = grpc.insecure_channel('{}'.format(workerip))
        req2 = node_pb2.nodeList()
        # req2.extend([])
        print("Workerip: ", workerip)
        stub = node_pb2_grpc.NodeCommunicationStub(channel)
        # req2.nodeips.append(workDistribution[workerip])
        req2.nodeips.extend(workDistribution[workerip])
        print("Req2: ", req2.nodeips)
        response2 = stub.updateNodeMonitorList(req2.nodeips)

        print("updated the node monitor list for remote ip ", response2)
        return response2

    def getNodes(self,masternodeip='localhost:50051'):
        ipstatus={}


        #get new nodes from master
        channel=grpc.insecure_channel('{}'.format(masternodeip))
        stub=replication_pb2_grpc.ReplicationStub(channel)
        req = replication_pb2.GetListOfNodesRequest()
        response =stub.GetListOfNodes(req,timeout = 3)
        response=str(response).split("\n")[:-1]
        print(response)
        for i in response:
            ip = i.split(":")[1].strip()[1:]+":"+i.split(":")[2].strip()[0:-1]
            print(ip)
            if ip not in ipstatus:
                ipstatus[ip]="up"
        print(ipstatus)
        return list(ipstatus.keys())



    def performLeaderJob(self):
        global nodesToMonitor
        global workDistribution
        leader_node = self.ip
        leader_node_ip=leader_node.split(':')[0]
        leader_node_port = leader_node.split(':')[1]
        # t1 = threading.Thread(target=self.s.serve, args=(self.ip))
        #
        # # starting thread 1
        # t1.start()
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
            # workdistribution={}
            global workDistribution
            # workDistribution = {}
            j=0
            while j<len(nodesToMonitor):
                nodeip=nodesToMonitor[j]
                #all nodes are distributed work

                if self.nodelist[i]!=self.ip:

                    if self.nodelist[i] not in workDistribution:
                        workDistribution[self.nodelist[i]]=[]
                    if nodeip not in workDistribution[self.nodelist[i]]:
                        workDistribution[self.nodelist[i]].append(nodeip)
                    i+=1
                    if i == len(self.nodelist):
                        i = 1
                    j+=1
                else:
                    i+=1

            for worker in workDistribution:
                self.nodeListUpdate(worker)
            # self.performMonitorJob()





    def performMonitorJob(self):
        global workDistribution
        while True:
            print("workDistribution: ", workDistribution)
            for worker in workDistribution:
                self.c.remote_call(worker)
                # self.c.nodeListUpdate(worker)


    def doJob(self):
        if self.state=="leader":
            self.term+=1
            self.performLeaderJob()
        else:
            self.performMonitorJob()

if __name__ == "__main__":
    nodesList = ["localhost:50061", "localhost:50062", "localhost:50063"]
    leader = Node("leader",nodesList[0],nodesList, "localhost:50051")
    # follower1 = Node("follower", nodesList[1], nodesList, "localhost:50051")
    # follower2 = Node("follower", nodesList[2], nodesList, "localhost:50051")