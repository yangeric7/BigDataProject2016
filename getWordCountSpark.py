from pyspark import SparkConf, SparkContext
import sys
import re

word_file = 'hdfs:///user/yange1/words'
name_file = 'names.txt'
MAX_WORDS = 10000
'''
This part of the code uses some of the homework 3 code with modifications to fit our data gathering
'''
def getWikiData(spark, listOfNames, wikiFile):
    importantWords = ['MVP', 'time', 'championship', 'award']
    names = spark.textFile(wikiFile)
    names = names.map(lambda line: get_title_and_text(line)) \
            .flatMap(lambda (name,text):[(name + ',' + word, 1) for word in text if word in importantWords and name in listOfNames]) \
            .reduceByKey(lambda x,y: x+y) \
            .saveAsTextFile(word_file)

def getListOfNames(namefile):
    listOfNames = []
    f = open(namefile)
    for line in f:
        name = line.rstrip()
        listOfNames.append(name)

    return listOfNames

def get_title_and_text(text):
    return (get_title(text), get_text(text))

def get_title(text):
    title = '<title>'
    title_end = '</title>'
    start = text.index(title) + len(title)
    end = text.index(title_end)
    return text[start:end]

def get_text(text):
    text_tag = '<text xml:space="preserve">'
    text_end = '</text>'
    start = text.index(text_tag) + len(text_tag)
    end = text.index(text_end)
    text_block = text[start:end]
    return re.sub(r"\W+", ' ', text_block).strip().split(' ')

if __name__ == '__main__':
    conf = SparkConf()
    if sys.argv[1] == 'local':
        conf.setMaster("local[3]")
        print 'Running locally'
    elif sys.argv[1] == 'cluster':
        conf.setMaster("spark://10.0.22.241:7077")
        print 'Running on cluster'

    conf.set("spark.executor.memory","10g")
    conf.set("spark.driver.memory","10g")
    spark = SparkContext(conf=conf)
    listOfNames = getListOfNames(name_file)
    getWikiData(spark,listOfNames,sys.argv[2])
