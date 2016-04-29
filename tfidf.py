from pyspark import SparkConf, SparkContext

import sys

'''
This portion of the code reflects the same tf_idf logic and code produced from 
homework 3
'''

word_file = 'hdfs:///user/yange1/words.txt'
tf_idf_file = 'hdfs:///user/yange1/tfidf.txt'

def tf_idf(spark):
	word_data = spark.textFile(word_file)
	lines = word_data.map(lambda line: eval(line)) \
			.map(lambda line: split_input(line))

	wordsindoc = lines.groupBy(lambda row: row[0]) \
				.flatMap(lambda x: list(x[1])) \
				.map(lambda x: (x[0],x[2])) \
				.reduceByKey(lambda x,y: x+y)

	termfreq = lines.keyBy(lambda x: x[0]) \
				.join(wordsindoc) \
				.map(lambda x: (x[1][0][0],x[1][0][1],float(x[1][0][2])/float(x[1][1])))

	distinctpages = lines.groupBy(lambda row: row[0]) \
					.map(lambda x: x[0]) \
					.count()

	invdocfreq = lines.groupBy(lambda row: row[1]) \
                 .map(lambda x: (x[0],len(list(x[1])))) \
                 .map(lambda x: (x[0],distinctpages/float(x[1])))
    
    tfidf = termfreq.keyBy(lambda x: x[1]) \
            .join(invdocfreq) \
            .map(lambda x: (x[1][0][0],x[0],x[1][0][2]*x[1][1])) \
            .sortBy(lambda x: (x[0],x[2])) \
            .saveAsTextFile(tf_idf_file)

def split_input(line):
	return line[0].split(',')[0], line[0].split(',')[1],line[1]


if __name__ == '__main__':
	conf = SparkConf()
	if sys.argv[1] == 'local':
		conf.setMaster("local[3]")
		print 'Running locally'
	elif sys.argv[1] == 'cluster':
		conf.setMaster("spark://10.0.22.241:7077")
		print 'Running on cluster'
	conf.set("spark.executor.memory", "10g")
	conf.set("spark.driver.memory", "10g")
	spark = SparkContext(conf=conf)
	tf_idf(spark)
