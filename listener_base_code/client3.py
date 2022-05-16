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


HOST3 = '10.0.0.215'
PORT3 = 50007
# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST3, PORT3))

# Create an instance of ProcessData() to send to server.
variable = ProcessData()
# Pickle the object and send it to the server
data_string = pickle.dumps(variable)
s.send(json.dumps({"ip":"333.333.333.33","status":"healthy"}))
s.close()
print('Data Sent from socket 3 to Server')


