import grpc
from concurrent import futures
import time

import calculator_pb2
import calculator_pb2_grpc

import root
class CalculatorService(calculator_pb2_grpc.CalculatorServicer):

    def Square(self,request,context):
        response=calculator_pb2.Number()
        print(request.value)
        response.value=root.square(request.value)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
