from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import Row
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import json

def mapper(line):
    fields = json.loads(line)
    return Row(logsource=str(fields['logsource']), \
               message=str(fields['message']))

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        spark = getSparkSessionInstance(rdd.context.getConf())
        rowRdd = rdd.map(lambda w: mapper(w[1]))

        wordsDataFrame = spark.createDataFrame(rowRdd)
        wordsDataFrame.createOrReplaceTempView("logs")

        wordCountsDataFrame = spark.sql("select logsource, count(*) as total from logs group by logsource")
        wordCountsDataFrame.show()
    except Exception, e:
        print(e)
    
 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: mytest.py <broker_list> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="mytest")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 10)

    brokers, topic = sys.argv[1:]
    stream = KafkaUtils.createStream(ssc, brokers, "spark-streaming-consumer", {topic:1})

    stream.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()

