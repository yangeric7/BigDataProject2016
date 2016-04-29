import wikipedia
import csv
import sys

index_file = 'hdfs:///user/yange1/wikipediadata.txt'

def getNames(textfile):
    names = []
    with open(textfile) as playerData:
        reader = csv.DictReader(playerData)
        for row in reader:
            name = row['Name']
            if name not in names:
                names.append(name)

    return names

def getWikiData(names):
    f = open(index_file, 'w')
    for name in anames:
        page = wikipedia.page(name)
        content = page.content
        wordCount = getWordCount(content)
        links = len(page.links)

        for word, count in wordCount:
            data = tuple(name,word,count)
            f.write(str(data) + '\n')

    f.close()

def getWordCount(content):
    importantWord = ['MVP','All-Star','championship','award']
    listOfWords = content.split(" ")
    wordCount = {}
    
    for word in listOfWords:
        if word in importantWords:
            if word in wordCount:
                wordCount[word] = wordCount[word] + 1
            else:
                wordCount[word] = 1

    return wordCount

if __name__ == '__main__':
    playerfile = sys.argv[1]
    listOfNames = getNames(playerfile)
    getWikiData(listOfnames)
