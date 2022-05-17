import threading
import client
import server

if __name__ == "__main__":
    # creating thread
    c=client.client()
    s=server.server()

    t1 = threading.Thread(target=s.serve, args=("localhost",500051))
    t2 = threading.Thread(target=c.remote_call, args=("localhost",500052))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    # both threads completely executed
    print("Done!")