from Person import *
from Coding import *
from Decoding import *


def pullServerSide(username, password, repository, path, type_):
    user = checkInfoUser(username, password)
    pathT = path
    if user is None:
        return None
    answer = getOwner(user, repository)
    last = os.getcwd()
    os.chdir("data/" + answer.getUsername() + "/" + repository)
    ans = encoder(type_, pathT)
    os.chdir(last)

    return ans


def OpullServerSide(username, repository, path, type_):
    last = os.getcwd()
    usernameTemp = username
    os.chdir("data/" + usernameTemp + "/" + repository)
    pathT = path
    ans = encoder(type_, pathT)
    os.chdir(last)
    return ans


def pushServerSide(username, password, messageBody, repository, commit_message):
    user = checkInfoUser(username, password)
    if user is None:
        return False
    answer = getOwner(user, repository)
    pathT = "data/" + answer.getUsername()
    pathT = pathT + "/" + repository
    decoder(messageBody, pathT, commit_message)
    return True


def getOwner(user, repository):
    repositories = user.getRepositories()
    answer = ""
    for x in repositories:
        if x == repository:
            return repositories[x]


def pullClientSide(path, type_, ready=True):
    if ready is False:
        return
    answer = encoder(type_, path)
    return answer


def pushClientSide(messageBody, path):
    if path is None:
        return False
    decoder(messageBody, path)
