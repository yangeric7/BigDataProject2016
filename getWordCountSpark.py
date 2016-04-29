from pyspark import SparkConf, SparkContext
import wikipedia
import sys

word_file = 'hdfs:///user/yange1/words.txt'

def getWikiData(spark, listOfNames):
    importantWord = ['MVP','All-Star','championship','award']
    
    names = spark.textFile(listOfNames)
    names = names.map(lambda line: getText(line)) \
            .flatMap(lambda (name,text):[(name + ',' + word, 1) if word in importantWord for word in text]) \
            .reduceByKey(lambda x,y: x+y) \
            .saveAsTextFile(word_file)

def getText(line):
    page = wikipedia.page(line)
    content = page.content

    return (line,content)

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
    getWikiData(spark,sys.argv[2])
