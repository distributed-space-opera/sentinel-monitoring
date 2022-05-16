import json
import socket, pickle

class ProcessData:
    process_id = 0
    project_id = 0
    task_id = 0
    start_time = 0
    end_time = 0
    user_id = 0
    weekend_id = 0



HOST = '10.0.0.215'
PORT = 50007
# Create a socket connection.
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT))

# Create an instance of ProcessData() to send to server.
variable1 = ProcessData()
# Pickle the object and send it to the server
data_string1 = pickle.dumps(variable1)
s1.send(json.dumps({"ip":"111.111.111.11","status":"healthy"}))

s1.close()
print('Data Sent from socket 1 to Server')