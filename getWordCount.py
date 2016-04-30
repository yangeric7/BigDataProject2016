import wikipedia
import csv
import sys

index_file = 'playerWikiData.csv'

def getNames(textfile):
    names = []
    f = open(textfile)
    for line in f:
        name = line.rstrip()
        names.append(name)

    return names

def getWikiData(names):
    f = open(index_file, 'w')
    for name in names:
        print name
        try:
            page = wikipedia.page(name)
        except wikipedia.exceptions.DisambiguationError as e:
            print e.options
            newsearch = name + '(basketball)'
            if newsearch in e.options:
                page = wikipedia.page(newsearch)
            else:
                continue
        links = len(page.links)
        f.write(name + ',' + str(links) + '\n')

    f.close()

if __name__ == '__main__':
    playerfile = sys.argv[1]
    listOfNames = getNames(playerfile)
    getWikiData(listOfNames)
