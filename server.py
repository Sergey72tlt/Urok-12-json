import socket
import time
import json

HOST = 'localhost'
PORT = 9090

quit = False
clients = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print('--- Сервер запущен ---')

while not quit:
    try:
        data, addr = sock.recvfrom(1024)
        current_time = time.strftime("%Y-%m-%d %H:%m:%S", time.localtime())
        if addr not in clients:
            clients.append(addr)
            result = json.loads(data)
            print("- - - - -", "\n", result["time"], "\n", result["action"],
                  "\n", "status -", result["status"], "\n", "name:", result["name"],
                  result["message"])
            code = 202
            data = {"response": "code: 202", "time": current_time, "name": result["name"],
                    "message": result["message"]}
            data1 = json.dumps(data).encode("utf-8")
            sock.sendto(data1, addr)
        else:
            result = json.loads(data)
            print("- - - - -", "\n", result["action"], "\n", result["time"], "\n",
                  "status", result["status"], "\n", result["name"], "::",
                  result["message"])
            code = 202
            data = {"response": "code: 202", "time": current_time, "name": result["name"],
                    "status": result["status"], "message": result["message"]}
            data1 = json.dumps(data).encode("utf-8")
            sock.sendto(data1, addr)

        for client in clients:
            if addr != client:
                data = {"response": "", "time": "", "name": result["name"],
                        "status": "", "message": result["message"]}
                data1 = json.dumps(data).encode("utf-8")
                sock.sendto(data1, client)
    except:
        print("----Server Stoped----")
        quit = True
sock.close()


