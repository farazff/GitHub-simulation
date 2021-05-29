import math
import socket
import sys
from MessageHandler import *

HOST = 'localhost'
PORT = 8787


def client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Unable to connect')
        sys.exit(-1)
    try:
        s.connect((HOST, PORT))
        while True:
            now = os.getcwd()
            print(now, " ", "$", end="")
            message = input()
            toSendMessage = createMessage(message)
            if toSendMessage == "":
                print("Invalid input!!!")
                continue
            size = str(len(toSendMessage.encode('utf-8')))
            s.sendall(size.encode('ascii'))
            s.sendall(toSendMessage.encode('ascii'))

            data = s.recv(2048)
            string_data = ""
            data = data.decode("ascii")
            for i in range(math.ceil(int(data) / 2048)):
                temp = s.recv(2048)
                temp = temp.decode()
                string_data = string_data + str(temp)

            if string_data.startswith("pprr"):
                string_data = string_data[4:]
                if string_data is None:
                    break
                pushClientSide(string_data, "./")
                print('SERVER:', "Action done")
            else:
                print('SERVER:', string_data)

    except socket.error:
        print('Client Error !!!')
    finally:
        s.close()


def createMessage(command):
    messageToSend = ""
    command = str(command)

    if command.startswith("signup"):
        name = input("Username: ")
        password1 = input("Password: ")
        password2 = input("Password: ")
        if password1 == password2:
            messageToSend = messageToSend + "a$"
            messageToSend = messageToSend + name + "$"
            messageToSend = messageToSend + password1 + "$"
        else:
            print("Password doesn't match\n\n")

    elif command.startswith("signin"):
        name = input("Username: ")
        password = input("Password: ")
        messageToSend = messageToSend + "b$"
        messageToSend = messageToSend + name + "$"
        messageToSend = messageToSend + password + "$"

    elif command.startswith("mkrepo"):
        parts = command.split()
        messageToSend = messageToSend + "c$"
        messageToSend = messageToSend + parts[1] + "$"

    elif command.startswith("list"):
        messageToSend = messageToSend + "d$"

    elif command.startswith("select"):
        parts = command.split()
        messageToSend = messageToSend + "e$"
        messageToSend = messageToSend + parts[1] + "$"

    elif command.startswith("push"):
        parts = command.split()
        commitMessage = command.split("\"")[1]
        data = pullClientSide(parts[-1][1:-1], parts[-2][1], ready=True)
        messageToSend = messageToSend + "f$" + commitMessage + "$"
        messageToSend = messageToSend + data + "$"

    elif command.startswith("pull"):
        parts = command.split()
        messageToSend = messageToSend + "g$"
        messageToSend = messageToSend + parts[-2][1] + "$"
        messageToSend = messageToSend + parts[2][1:-1] + "$"

    elif command.startswith("viewcm"):
        messageToSend = "h$"

    elif command.startswith("sync"):
        messageToSend = messageToSend + "i$"

    elif command.startswith("userslist"):
        messageToSend = messageToSend + "j$"

    elif command.startswith("cont"):
        parts = command.split()
        messageToSend = messageToSend + "k$"
        messageToSend = messageToSend + parts[1] + "$"

    elif command.startswith("Opull"):
        parts = command.split()
        messageToSend = messageToSend + "l$"
        messageToSend = messageToSend + parts[1] + "$"
        messageToSend = messageToSend + parts[2] + "$"
        messageToSend = messageToSend + parts[3][1] + "$"
        messageToSend = messageToSend + parts[4][1:-1] + "$"

    elif command.startswith("repolsof"):
        parts = command.split()
        messageToSend = messageToSend + "m$"
        messageToSend = messageToSend + parts[1] + "$"

    return messageToSend


if __name__ == '__main__':
    local_dir = input("Enter the address you Local directory: ")
    os.chdir(local_dir)
    client()
