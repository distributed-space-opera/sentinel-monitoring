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
leaderip=""
workerList={}
processId=-1
class NodeCommunicationService(node_pb2_grpc.NodeCommunicationServicer):


    def setLeader(self, request, context):
        global leaderip
        leaderip=request.nodeip
        reply=node_pb2.updateLeaderResponse()
        reply.status = "ok"
        return reply


    def GetNodes(self, request, context):
        global workDistribution
        reply = node_pb2.GetListOfNodesResponse()
        reply.nodeips.extend(workDistribution[request.nodeip])
        return reply


    def updateNodeMonitorList(self, request, context):
        global workDistribution
        print("update Node: -->", request.nodeips)
        workDistribution = request.nodeips

        reply = node_pb2.updateNodeListResponse()
        reply.status="ok"
        return reply

    def proposeLeader(self, request, context):
        remote_process_id=request.processId
        reply = node_pb2.proposeLeaderResponse()
        global processId
        if remote_process_id>processId:
            reply.status="ok"
        else:
            reply.status="deny"
        return reply


    def updateLeader(self, request, context):
        global leaderip
        print("updating the leader to -----> ",request.nodeip)
        leaderip =request.nodeip
        reply=node_pb2.updateLeaderResponse()
        reply.status="ok"
        return reply
    def checkLeader(self, request, context):
        reply=node_pb2.generalResponse()
        reply.status="ok"
        return reply

    def checkMonitor(self, request, context):
        reply=node_pb2.generalResponse()
        reply.status="ok"
        return reply



class server:
    def __init__(self,nam):
        self.name=nam



    def serve(self,ip,port):

        print("server runnning now " + self.name)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeCommunicationServicer_to_server(NodeCommunicationService(), server)
        server.add_insecure_port('{}:{}'.format(ip,port))
        server.start()
        server.wait_for_termination()




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




            time.sleep(3)



        return "up"

    def sendDownRequest(ip, masterip="localhost", masterport=50051):
        channel=grpc.insecure_channel("localhost:50051")
        req2 = replication_pb2.NodeDownUpdateRequest()

        stub=replication_pb2_grpc.ReplicationStub(channel)

        req2.nodeip=bytes(str(ip),"utf-8")
        print("--------------received the {} ".format(str(ip)))
        print("---------------converted into {} ".format(req2.nodeip))
        response2 = stub.NodeDownUpdate(req2)

        print("response received from the server is",response2)
        return response2

class Node:
    def __init__(self,state,ip,nodelist,masternodeip,process_id):
        self.state=state
        self.term=0
        self.ip=ip
        self.nodelist=nodelist
        self.masternodeip=masternodeip
        self.c = client("client")
        global processId
        global workerList
        processId = process_id
        for node in nodelist:
            workerList[node]="up"
        # self.masternodeport = masternodeport
    def server_listen(self,ip,port):
        self.s = server("node")
        self.s.serve(ip,port)
    def nodeListUpdate(self, workerip):
        global workDistribution
        channel = grpc.insecure_channel('{}'.format(workerip))
        req2 = node_pb2.nodeList()
        stub = node_pb2_grpc.NodeCommunicationStub(channel)
        # req2.nodeips.append(workDistribution[workerip])
        req2.nodeips.extend(workDistribution[workerip])
        response2 = stub.updateNodeMonitorList(req2)
        return response2
    def setLeader(self,workerip):
        global workDistribution
        global leaderip
        channel = grpc.insecure_channel('{}'.format(workerip))
        req2 = node_pb2.newLeaderRequest()
        req2.nodeip=leaderip
        stub = node_pb2_grpc.NodeCommunicationStub(channel)

        response2 = stub.setLeader(req2)

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

            workernum=len(self.nodelist)
            i=0
            # workdistribution={}
            global workDistribution
            global workerList
            workDistribution = {}
            j=0
            print("here is the monitor status",workerList)
            nodesToMonitor = self.getNodes(self.masternodeip)
            print("as a leader I have to redistribute this  ",nodesToMonitor)
            print(" Here is the monitor list",self.nodelist)

            while j<len(nodesToMonitor):
                nodeip=nodesToMonitor[j]
                #all nodes are distributed work
                if i==len(self.nodelist):
                    i=0
                if self.nodelist[i]!=self.ip:
                    if self.checkOnMonitor(self.nodelist[i])=="down":
                        print("This monitor {} is down".format(self.nodelist[i]))
                        i+=1
                        continue
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
                self.setLeader(worker)
                time.sleep(2)
            # self.performMonitorJob()
            time.sleep(10)


#cd .\sentinel-monitoring\bidirectional_multithread\


    def checkOnLeader(self):
        global leaderip
        channel=grpc.insecure_channel('{}'.format(leaderip))
        req = node_pb2.generalPingRequest()
        stub=node_pb2_grpc.NodeCommunicationStub(channel)
        # print('{}:{}'.format(ip, port))
        failed_attempts=0
        while True:
            try:
                response=stub.checkLeader(req,timeout = 3)
                print("successful response ",response)
                time.sleep(5)
                return "up"

            except Exception as e:
                failed_attempts+=1
                if failed_attempts!=3:
                    continue
                print("Process failed")
                if failed_attempts==3:
                    print("Failed far too many times. Gang leader down")
                    failed_attempts=0
                    return "down"




            time.sleep(3)

    def checkOnMonitor(self,workerip):

        channel=grpc.insecure_channel('{}'.format(workerip))
        req = node_pb2.generalPingRequest()
        stub=node_pb2_grpc.NodeCommunicationStub(channel)
        # print('{}:{}'.format(ip, port))
        failed_attempts=0
        while True:
            try:
                response=stub.checkMonitor(req,timeout = 3)
                print("successful response ",response)
                time.sleep(5)
                return "up"

            except Exception as e:
                failed_attempts+=1
                if failed_attempts!=3:
                    continue
                print("Process failed")
                if failed_attempts==3:
                    print("Failed far too many times. Gang leader down")
                    failed_attempts=0
                    return "down"




            time.sleep(3)


    def proposeLeader(self,workerip):
        global processId
        channel = grpc.insecure_channel('{}'.format(workerip))
        req2 = node_pb2.proposeLeaderRequest()
        req2.processId = processId
        req2.nodeip = self.ip
        stub = node_pb2_grpc.NodeCommunicationStub(channel)
        # req2.nodeips.append(workDistribution[workerip])
        response2 = stub.proposeLeader(req2)
        return response2




    def performMonitorJob(self):
        global workDistribution
        global leaderip
        flag=0
        currlist=[]
        while True:
            #print("workDistribution:--> ", workDistribution)

            for worker in workDistribution:
                resp = self.c.remote_call(worker)
                if resp=="down":
                    print(worker)
                    channel=grpc.insecure_channel("localhost:50051")
                    req2 = replication_pb2.NodeDownUpdateRequest()
                    stub=replication_pb2_grpc.ReplicationStub(channel)
                    req2.nodeip=worker
                    response2 = stub.NodeDownUpdate(req2)

                    print("response received from the server is",response2)


                # self.c.nodeListUpdate(worker)
            if len(workDistribution)>0:
                x= self.checkOnLeader()
                if x =="down":

                    print("detected that the leader is down")

                    currlist = self.nodelist
                    if leaderip in currlist:
                        currlist.remove(leaderip)
                    if self.ip in currlist:
                        currlist.remove(self.ip)
                    count=0

                    for colleague in currlist:
                        response= self.proposeLeader(colleague)
                        if response.status=="ok":
                            count+=1
                        if count>len(currlist)//2 : #gets majority
                            flag=1
                            currlist.append(self.ip)
                            self.nodelist=currlist
                            break
                    if flag==1:
                        break

            time.sleep(10)
        if flag==1:
            print("here is the self.nodelist to ", self.nodelist)
            print("here is the current list ", currlist)
            global workerList
            if leaderip in workerList:
                workerList[leaderip]="down"
            self.state="leader"
            #self.nodelist.remove(leaderip)
            execute()

                #propose itself as a new leader






    def doJob(self,role):
        global leaderip
        if role=="leader":
            leaderip=self.ip
            self.term+=1
            self.performLeaderJob()
        else:
            print("I am a follower")
            self.performMonitorJob()

def execute(ipnum=0,role="leader",listen_port=50061,processid=0):
    print("role received ",role)
    nodesList = ["localhost:50061", "localhost:50062", "localhost:50063"]
    leader = Node(role,nodesList[ipnum],nodesList, "localhost:50051",processid)
    t1 = threading.Thread(target=leader.server_listen, args=("localhost",listen_port))
    t1.start()

    t2 = threading.Thread(target=leader.doJob(role))
    t2.start()
    t1.join()
    t2.join()
#execute()
    # follower1 = Node("follower", nodesList[1], nodesList, "localhost:50051")
    # follower2 = Node("follower", nodesList[2], nodesList, "localhost:50051")