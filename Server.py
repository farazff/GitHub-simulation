import math
import socket
import threading
from copy import *
from MessageHandler import *

HOST = "127.0.0.1"
PORT = 8787


class ClientThread(threading.Thread):
    def __init__(self, address, client_socket, num):
        threading.Thread.__init__(self)
        self.address = address
        self.connection = client_socket
        self.num = num
        print("connection started with: ", address)

    def run(self):
        username = password = current_repository = None
        while True:
            data = self.connection.recv(2048)
            data = data.decode()
            string_data = ""
            for i in range(math.ceil(int(data) / 2048)):
                temp = self.connection.recv(2048)
                temp = temp.decode()
                string_data = string_data + str(temp)
            if not string_data:
                break
            answer = parseReceivedMessage(string_data, checkInfoUser(username, password), current_repository)

            if type(answer) == list and len(answer) == 1:
                current_repository = answer[0]
                answer = "Repository selected"

            if type(answer) == list and len(answer) == 2:
                UN = answer[0]
                PS = answer[1]
                username = copy(UN)
                password = copy(PS)
                answer = "User logged in"

            if answer is None:
                answer = "ERROR"
            size = len(answer.encode('UTF-8'))
            self.connection.sendall(str(size).encode('ascii'))
            self.connection.sendall(bytes(answer, 'UTF-8'))

        self.connection.close()
        print("client disconnected")


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        count = 0
        print("Server is on!")
        while True:
            s.listen(1)
            connection, address = s.accept()
            new_thread = ClientThread(address, connection, count)
            new_thread.start()


def parseReceivedMessage(command, user, current_repository):
    parts = command.split("$")
    action = parts[0]
    print("action: ", action)
    if action == 'a' and user is None:
        ans = createNewUser(parts[1], parts[2])
        if not ans:
            return "User exists"
        return "User created"

    if action == 'b' and user is None:
        user = checkInfoUser(parts[1], parts[2])
        if user is None or user is False:
            return "No such user"
        return [user.getUsername(), user.getPassword()]

    if action == 'c':
        if user is None:
            return "Sign in first"
        createRepositoryForUser(user.getUsername(), user.getPassword(), parts[1])
        return "Repository created"

    if action == 'd':
        if user is None:
            return "Sign in first"
        repositories = user.getRepositories()
        if len(repositories) == 0:
            return "You don't have any repository"
        answer = ""
        for x in repositories:
            answer = answer + "\n" + str(x)
        return answer

    if action == 'e':
        if user is None:
            return "sign in first"
        if current_repository is not None:
            respond = "Your are currently in a repository"
            return respond
        repository_name = parts[1]
        repositories = user.getRepositories()
        found = False
        if len(repositories) == 0:
            return "You don't have any repository"
        for RN in repositories:
            if str(repository_name) == str(RN):
                found = True
                break
            found = False
        if not found:
            return "There isn't any repository with that name"
        return [repository_name]

    if action == 'f':
        if user is None:
            return "Sign in first"
        if current_repository is None:
            return "First choose a repository"
        pushServerSide(user.getUsername(), user.getPassword(), parts[2], current_repository, parts[1])
        return "Pushed successfully"

    if action == 'g':
        if user is None:
            return "Sign in first"
        if current_repository is None:
            return "First choose a repository"
        body = pullServerSide(user.getUsername(), user.getPassword(), current_repository, parts[2], parts[1])
        return "pprr" + str(body)

    if action == 'h':
        if user is None:
            return "Sign in first"
        if current_repository is None:
            return "First choose a repository"
        try:
            add = "data/" + user.getUsername() + "/" + current_repository + "/commits.txt"
            with open(add, "r") as o:
                return o.read()
        except FileExistsError and FileNotFoundError:
            return "Commit file not found!"

    if action == 'i':
        if user is None:
            return "Sign in first"
        if current_repository is None:
            return "First choose a repository"
        body = pullServerSide(user.getUsername(), user.getPassword(), current_repository, "./", "-d")
        return "pprr" + str(body)

    if action == 'j':
        users = loadUsers()
        print(type(users))
        ans = ""
        for i in users:
            ans = ans + "\n" + i.getUsername()
        return ans

    if action == 'k':
        if user is None:
            return "Sign in first"
        if current_repository is None:
            return "First choose a repository"
        returnValue = addContributor(user.getUsername(), user.getPassword(), parts[1], current_repository)
        if returnValue is True:
            return "Added successfully"
        return "There isn't any user with that username"

    if action == 'l':
        if user is None:
            return "Sign in first"
        body = OpullServerSide(parts[1], parts[2], parts[4], parts[3])
        return "pprr" + str(body)

    if action == 'm':
        if user is None:
            return "Sign in first"
        users = loadUsers()
        foundedUser = None
        for user_ in users:
            if user_.getUsername() == parts[1]:
                foundedUser = user_
                break
        if foundedUser is not None:
            repositories = foundedUser.getRepositories()
            answer = ""
            for repo in repositories:
                answer = answer + "\n"
                answer = answer + str(repo)
            return answer

        return "No such user"


if __name__ == '__main__':
    server()
