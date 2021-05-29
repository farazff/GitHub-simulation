import os
import zlib
from base64 import *


def encoder(_type, path):
    outputContent = ""
    if "f" in _type:
        outputContent = outputContent + "f\n" + path + "\n"
        outputContent = outputContent + fileEncoder(path) + "\nfinish"

    elif "d" in _type:
        outputContent = outputContent + "d"
        outputContent = outputContent + directoryEncoder(path) + "\nfinish"

    return outputContent


def directoryEncoder(path):
    outputContent = ""
    lists = os.listdir(path)
    for fileName in lists:
        if os.path.isfile(path + "/" + fileName):
            tmpPath = path + "/"
            tmpPath = tmpPath + fileName
            outputContent = outputContent + "\n" + tmpPath + "\n"
            outputContent = outputContent + fileEncoder(tmpPath)
        else:
            outputContent = outputContent + directoryEncoder(path + "/" + fileName)
    return str(outputContent)


def fileEncoder(path):
    with open(path, 'rb') as inputFile:
        rawData = inputFile.read()
        encodedData = b64encode(rawData)
        rawDataString = ""
        compressedData = zlib.compress(encodedData, 1)

        for i in compressedData:
            rawDataString = rawDataString + str(i)
            rawDataString = rawDataString + " "
        rawDataString = rawDataString[0:len(rawDataString) - 1]
        return rawDataString
