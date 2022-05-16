import grpc

import calculator_pb2
import calculator_pb2_grpc

channel=grpc.insecure_channel('localhost:50051')
number = calculator_pb2.Number(value=15)
stub=calculator_pb2_grpc.CalculatorStub(channel)
response=stub.Square(number)
print(response.value)