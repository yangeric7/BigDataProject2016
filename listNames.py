import csv
import sys
import subprocess

name_file = 'names.txt'

def listNames(fileName):
    names = []
    cat = subprocess.Popen(["hadoop", "fs", "-cat", fileName], stdout=subprocess.PIPE)
    for line in cat.stdout:
        newLine = line.split(",")
        name = newLine[1].strip('*')
        if name != 'Player' and name not in names:
            names.append(name)
    return names

def writeToFile(names):
    f = open(name_file, 'w')
    for name in names:
        f.write(name + '\n')

if __name__ == '__main__':
    fileName = sys.argv[1]
    names = listNames(fileName)
    writeToFile(names)
