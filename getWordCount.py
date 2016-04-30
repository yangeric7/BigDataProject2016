import wikipedia
import csv
import sys

index_file = 'testwordcount.txt'

def getNames(textfile):
    names = []
    with open(textfile) as playerData:
        reader = csv.DictReader(playerData)
        for row in reader:
            name = row['Player']
            if name not in names:
                names.append(name)

    return names

def getWikiData(names):
    f = open(index_file, 'w')
    for name in names:
        try:
            page = wikipedia.page(name)
        except wikipedia.exceptions.DisambiguationError as e:
            print e.options
            newsearch = name + '(basketball)'
            if newsearch in e.options:
                page = wikipedia.page(newsearch)
            else:
                continue
        content = page.content
        wordCount = getWordCount(content)
        links = len(page.links)

        for word in wordCount:
            print word;
            data = (name,word,wordCount[word])
            f.write(str(data) + '\n')

    f.close()

def getWordCount(content):
    importantWords = ['MVP','All-Star','championship','award']
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
    getWikiData(listOfNames)
