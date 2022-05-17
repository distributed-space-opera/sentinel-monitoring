import time
import grpc
import healthcheck_pb2
import healthcheck_pb2_grpc
import replication_pb2
import replication_pb2_grpc


class client:
    def __init__(self):
        pass
    def remote_call(self,ip,port):
        print("client called")
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
