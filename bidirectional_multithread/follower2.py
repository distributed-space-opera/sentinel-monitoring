from leader import execute

if __name__ == "__main__":
    nodesList = ["localhost:50061", "localhost:50062", "localhost:50063"]
    #follower1 = Node("follower", nodesList[2], nodesList, "localhost:50051")
    execute(2,"follower",50063,2)