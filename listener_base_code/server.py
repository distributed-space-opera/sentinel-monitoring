# -*- coding: utf-8 -*-
"""
Created on Sat May 14 18:05:20 2022

@author: 16692
"""

import socket, pickle
import json
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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print("Connected by")

data = conn.recv(4096)
#data_variable = pickle.loads(data)
conn.close()
print(json.loads(data))
# Access the information by doing data_variable.process_id or data_variable.task_id etc..,
print('Data received from client')