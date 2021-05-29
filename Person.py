import os
import pickle


class Person:
    __cc = 0

    def __init__(self, username, password, create=True):
        self.__username = username
        if password is None:
            password = "1234"
        Person.__cc += 1
        self.__password = password
        self.create = create
        self.__repositories = dict()

    def getUsername(self):
        return self.__username

    def getRepositories(self):
        return self.__repositories

    def checkPassword(self, password):
        if password is None:
            raise TypeError("Invalid password")
        if self.__password == password:
            return True
        return False

    def getPassword(self):
        if self.__password is None:
            return None
        return self.__password

    def __eq__(self, other):
        return self.__username == other.getUsername()

    def addRepository(self, repository_name, selfOwner=True, ownerUser=None, contribute=False):
        if selfOwner is True:
            self.__repositories[repository_name] = self
            return
        else:
            self.__repositories[repository_name] = ownerUser

    @classmethod
    def printCounter(cls):
        print(cls.__cc)


def checkInfoUser(username, password):
    if username is None or password is None:
        return None
    users = loadUsers()

    for user in users:
        if user.getUsername() == username and user.checkPassword(password):
            return user

    return None


def createNewUser(username, password):
    users = loadUsers()

    new_user = Person(username, password)

    for user in users:
        if new_user == user:
            return False
    saveUsers(users)
    users.append(new_user)
    saveUsers(users)
    userLocal = new_user.getUsername()
    database = "./data"
    path = os.path.join(database, userLocal)
    try:
        os.mkdir(path)
    except OSError:
        return False

    return True


def loadUsers():
    file = None
    path = './data/usersList.raw'
    try:
        file = open(path, 'rb')
        users = pickle.load(file)
    except IOError:
        users = []
    finally:
        if file is not None:
            file.close()

    return users


def saveUsers(users):
    file = None
    path = './data/usersList.raw'
    if users is None:
        return False
    try:
        file = open(path, 'wb')
        pickle.dump(users, file)
        file.close()
    except IOError as error:
        print(error)


def createRepositoryForUser(username, password, repository_name):
    user = checkInfoUser(username, password)
    path = './data'
    users = loadUsers()
    if user is None:
        return False
    baseDirectory = user.getUsername()
    if password is None:
        return False
    path = os.path.join(path, baseDirectory, repository_name)
    if repository_name is None:
        return False
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
    if user is None:
        return False

    for user_ in users:
        if user_ == user:
            user_.addRepository(repository_name)
            saveUsers(users)
            break
    saveUsers(users)
    return True


def addContributor(username, password, new_user_username, repository):
    print(username, password, new_user_username, repository)
    user = checkInfoUser(username, password)
    users = loadUsers()
    if user is None:
        return False

    if repository is None:
        return False

    for user_ in users:
        if user_.getUsername() == new_user_username:
            saveUsers(users)
            user_.addRepository(repository, selfOwner=False, ownerUser=user)
            saveUsers(users)
            return True

    return False
