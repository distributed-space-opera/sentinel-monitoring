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
PORT1 = 50007
PORT2 = 50008


def define_socket(HOST='10.0.0.215',PORT=50009):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    return s
    


s2=define_socket(HOST, PORT2)
#s1.listen(1)
#s2.listen(2)
#conn, addr = s1.accept()
#conn2, addr2 = s2.accept()

s1=define_socket(HOST, PORT1)
s1.listen(1)    

while True:
    print("Connected now")  
    conn, addr = s1.accept()
    data = conn.recv(4096)
    print(addr[0])
    
    
    #data_variable = pickle.loads(data)
    if data!=b'':
        print(json.loads(data))
    print("data from socket 2 now")
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    print('Data received from client')
    print('Exit now?')
    conn.close()
#conn2.close()






#monitoring registry


    