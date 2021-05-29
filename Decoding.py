import os
import zlib
from base64 import *
from datetime import *


def decoder(messageBody, basePath, commit_message=None):
    bodyList = str(messageBody).split("\n")
    receivedFiles = {}

    temp = bodyList[0]
    temp2 = bodyList[1]
    if "f" in temp:
        receivedFiles[temp2] = bodyList[2]
    elif "d" in temp:
        counter = 1
        while True:
            if "finish" in bodyList[counter]:
                break
            temp = bodyList[counter]
            receivedFiles[temp] = bodyList[counter + 1]
            counter += 1
            counter += 1

    for key in receivedFiles.keys():
        try:
            path = basePath + "/"
            temp = key.split('/')[0:-1]
            path = path + "/".join(temp)
            os.makedirs(path)

            rawDataString = receivedFiles[key].split(" ")
            for i in range(len(rawDataString)):
                rawDataString[i] = int(rawDataString[i])
            compressedData = bytes(rawDataString)
            uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(uncompressedData)
            nowPath = basePath + "/"
            nowPath = nowPath + key
            with open(nowPath, 'wb') as outputFile:
                outputFile.write(decodedData)

        except FileExistsError:
            rawDataString = receivedFiles[key].split(" ")
            len1 = len(rawDataString)
            for i in range(len1):
                rawDataString[i] = int(rawDataString[i])

            compressedData = bytes(rawDataString)
            uncompressedData = zlib.decompress(compressedData)
            decodedData = b64decode(uncompressedData)
            thisPath = basePath + "/" + key
            with open(thisPath, 'wb') as outputFile:
                outputFile.write(decodedData)

    if commit_message is None:
        pass
    if commit_message is not None:
        try:
            thisPath = basePath + "/" + "commits.txt"
            with open(thisPath, "a") as commit:
                commit.write("{}|{}\n".format(commit_message, datetime.now()))
        except FileExistsError:
            print("Commits not found")
