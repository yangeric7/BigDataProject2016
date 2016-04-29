from mrjob.job import MRJob
import wikipedia

class WordCount(MRJob):
    def mapper(self, _, line):
        name = line[0]
        page = wikipedia.page(name)
        wordDict = counter(page.content)
        for word,count in wordDict:
            yield [name,word],count

    def reducer(self,key,counts):
        name = key[0]
        word = key[1]
        yield name + ',' + word, counts


def counter(content):
    importantWords = ['MVP','All-Star','championship', 'award']
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
    WordCount.run()
