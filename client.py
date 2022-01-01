from socket import SOCK_DGRAM, socket, AF_INET
import time
import threading
import json

shutdown = False
join = False
SERVER = ("localhost", 9090)


def receving(sock: socket):
    while not shutdown:
        data, addr = sock.recvfrom(1024)
        result1 = json.loads(data)
        print("- - - - -", "\n", result1["response"], "\n", result1["time"],
              "\n", "name:", result1["name"], "\n", "status: online", "\n", result1["name"],
              "::", result1["message"], "\n", "- - - - -")


sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("localhost", 0))

name = input("Name: ")

rt = threading.Thread(target=receving, args=(sock,))
rt.start()

while not shutdown:
    try:
        if not join:
            current_time = time.strftime("%Y-%m-%d %H:%m:%S", time.localtime())
            message1 = {"action": "new client conected", "time": current_time,
                        "name": name, "status": "online", "message": " "}
            data = json.dumps(message1).encode("utf-8")
            sock.sendto(data, SERVER)
            join = True
        else:
            time.sleep(1)
            message = input("[You] :: ")

            if message != "":
                current_time = time.strftime("%Y-%m-%d %H:%m:%S", time.localtime())
                message2 = {"action": "msg_from_chat", "time": current_time,
                            "name": name, "status": "online", "message": message}
                data = json.dumps(message2).encode("utf-8")
                sock.sendto(data, SERVER)
    except:
        sock.sendto(f"[{name}] <= Left Chat".encode("utf-8", SERVER))
        shutdown = True

rt.join()
sock.close()
