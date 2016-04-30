import sys

csv_file = 'playerWikiData.csv'

#this method turns the tfidf count for words into a dictionary of dictionaries 
#such that each player is a key in the outer dictionary and the inner dictionary is the list of specific words
#if a player doesn't have a tfidf for that word, give it a value of -1
def get_tfidf_count(filename):
    importantWords = ['MVP','time','championship','award']
    f = open(filename)
    playerData = {}
    for line in f:
        data = line.rstrip().split(",")
        name,word,count = data
        if name not in playerData:
            playerData[name] = {word:count}
        else:
            playerData[name][word] = count
        
    for key,value in playerData.iteritems():
        for word in importantWords:
            if word not in value:
                playerData[key][word] = "-1"
    return playerData

def writeToFile(playerDict):
    f = open(csv_file,'w')
    
    for name,value in playerDict.iteritems():
        counts = ','.join(str(count) for word,count in value.iteritems())
        print name + ','.join(str(word) for word,count in value.iteritems())
        playerData = name + ',' + counts + '\n'
        f.write(playerData)
        

if __name__ == '__main__':
    filename = sys.argv[1]
    playerDict = get_tfidf_count(filename)
    writeToFile(playerDict)
