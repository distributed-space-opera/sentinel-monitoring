from leader import Node

if __name__ == "__main__":
    nodesList = ["localhost:50061", "localhost:50062", "localhost:50063"]
    follower1 = Node("follower", nodesList[1], nodesList, "localhost:50051")