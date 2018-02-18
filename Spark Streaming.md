# Spark Streaming
Processing continuous streams of data in near-real-time 
## Why?
- Big data never stops coming
- Analyze data streams in real-time instead of in a huge batch jobs daily
- Analyze streams of web log data to react to user behaviour
- Analyze streams of real-time sensor data for Internet of Things stuff

## Spark Streaming High Level
datastreams ===> receivers ===> RDD --> RDD --> RDD (Batches of data for a given time increment ===> Transform & output to other systems
Datastreams = flume, kafka etc..
spark cluster have bunch of receivers
when data comes it discretizes into little chunks with batch increments  by 1 sec or whatever increment etc...
so each RDD within that stream of data  contains some discretized chunk of data recieved over some small timeperiod , from there we transform that data
and process it across the rdd in clusters
-- Really micro batches
-- practically its streaming
* Processing of RDD's can be parallel on different worker nodes

## Dstreams (Discretized Streams)
- Generates the RDD's for each time step, can produce output at each time step
- Can be transformed and acted on in much the same way as RDD
- or you can access their underlying RDD's if you need them

## Spark vs Spark steaming
- Spark steaming: perform operations on DSperform operations on DStream and that gets applied everytime new data is received in the batch and then you kikk off go run forever until I stop
- Spark : get an RDD that represents everything in my cluster for whatever I looked up, process it all once and I'm done

- Dtream you can still transform map things perform actions just like you would on RDD.

### Common Stateless trasformations on DStreams
- Map
- FlatMap
- Filter
- reducebyKey

### stateful data
you can also maintain a long-lived state on DStream.
For example - running totals, broken down by keys
Another example: aggregating session data on web activity
That is done by technique called - "Windowing"

### Windowed Transformations
- Allows you to compute results across a longer time period than your batch interval
- Example: Topsellers from past 1 hour
- you might process data every one second
- But maintains a window for 1 hour
- The window "slides" as the time goes on, to represent batches within the window

### Batch Interval vs Slide Interval vs Window interval
- Batch interval is how often is captured into a DStream
- Slide interval is how often a windowed transformation is computed
- The window interval is how far back in the time the windowed transformation goes

eg: - best seller Batch1 sec , Slide30mts window1 hour

### windowed transformations: code
The batch interval is set up with your SparkContext:
ssc  = StreamingContext(sc,1)
you can use reduceByWindow() or reduceByKeyAndWindow() to aggregate data across a longer period of time!

hashtagCounts= hashtagKeyValues.reduceByKeyAndWindow(lambda x,y:x+y, lambda x,y:x-y, 300,1)
adding
substracting
window interval of 300 secs
slide interval of 1 sec & batch interval is also 1 sec

every 1 sec goback 5mts count something thats in DStream hashtag key values & print

# Structured Streaming
- A new high-level API for streaming structured data
- Use data sets, but with more explicit type of information
- A data frame is really a data set(Row) 
instead of dealing with individual RDD's use data streams in a sructured tabular fashion and it goes on never ending table

## Advantages over general streaming
- streaming code looks similar to non-streaming
- MlLib is also moving towards dataset library
- structured streaming into Machine Learning real time ***** etc..

### once you have SparkSession, you can stream data, query it, and write out the results
``` scala
val inputDF = spark.readStream.json("s3://logs")
inputDF.groupBy($"action", window($"time","1hour")).count().writeStream.format("jdbc").start("jdbc:mysql//..")

```

### for now stick with Dstream instead of structured streaming as it is still in Beta versions

- We' ll set up Flume to use a spooldir source as before
- But use an Avro Sink to connect through our spark streaming job - use a window to aggregate how often each url appears from our access logs
- using Avro in this manner is a "Push" mechanism to spark streaming, you can also "pull" data by using a custom sink for spark streaming

Logs ==> source(spool dir) ===>channel(memory) ===>sink (Avro) ====> Spark Streaming ====> console

## Previously with Flume we have configured the data into HDFS now lets do it into Avro, which is a communication protocol
wget media.sundog-soft.com/hadoop/sparkstreamingflume.conf

## python program for spark streaming
wget http://media.sundog-soft.com/hadoop/SparkFlume.py

``` python
import re

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.flume import FlumeUtils

parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]
pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

def extractURLRequest(line):
    exp = pattern.match(line)
    if exp:
        request = exp.groupdict()["request"]
        if request:
           requestFields = request.split()
           if (len(requestFields) > 1):
                return requestFields[1]


if __name__ == "__main__":

    sc = SparkContext(appName="StreamingFlumeLogAggregator")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 1)

    flumeStream = FlumeUtils.createStream(ssc, "localhost", 9092)

    lines = flumeStream.map(lambda x: x[1])
    urls = lines.map(extractURLRequest)

    # Reduce by URL over a 5-minute window sliding every second
    urlCounts = urls.map(lambda x: (x, 1)).reduceByKeyAndWindow(lambda x, y: x + y, lambda x, y : x - y, 300, 1)

    # Sort and print the results
    sortedResults = urlCounts.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))
    sortedResults.pprint()
    
    ssc.checkpoint("/home/maria_dev/checkpoint")
    ssc.start()
    ssc.awaitTermination()

```
### Run SparkStreaming code
[maria_dev@sandbox-hdp ~]$ vi SparkFlume.py 
[maria_dev@sandbox-hdp ~]$ mkdir checkpoint
[maria_dev@sandbox-hdp ~]$ ls
access_log_small.txt  flumelogs.conf       presto-server-0.194.tar.gz  spool
CassandraSpark.py     job.properties       SparkFlume.py               u.data
checkpoint            ml-100k              sparkstreamingflume.conf    u.data.1
example.conf          presto-server-0.194  spark-warehouse
[maria_dev@sandbox-hdp ~]$ spark-submit --packages org.apache.spark:spark-streaming-flume_2.11:2.2.0 SparkFlume.py 

### RUn FLume agent
[maria_dev@sandbox-hdp flume-server]$ bin/flume-ng agent --conf conf --conf-file ~/sparkstreamingflume.conf --name a1 -Dflume.root.logger=INFO,console

### Lets get a big log file
wget http://media.sundog-soft.com/hadoop/access_log.txt
 
### copy that to spool directory where flume is listening
[maria_dev@sandbox-hdp ~]$ cp access_log.txt spool/log22.txt

Now you will observe, Flume takes it & provides to spark & spark analyzes it & prints results in a window interval that we specified
------------------------------------------
Time: 2018-02-18 21:27:20
-------------------------------------------
(u'/xmlrpc.php', 31106)
(u'/wp-login.php', 1893)
(u'/', 336)
(u'/blog/', 100)
(u'/robots.txt', 93)
(u'/sitemap_index.xml', 87)
(u'/post-sitemap.xml', 87)
(u'/page-sitemap.xml', 86)
(u'/category-sitemap.xml', 86)
(u'/orlando-headlines/', 71)
...

-------------------------------------------
Time: 2018-02-18 21:27:21
-------------------------------------------
(u'/xmlrpc.php', 68415)
(u'/wp-login.php', 1923)
(u'/', 440)
(u'/blog/', 138)
(u'/robots.txt', 123)
(u'/sitemap_index.xml', 118)
(u'/post-sitemap.xml', 118)
(u'/page-sitemap.xml', 117)
(u'/category-sitemap.xml', 117)
(u'/orlando-headlines/', 95)
...

-------------------------------------------
Time: 2018-02-18 21:27:22
-------------------------------------------
(u'/xmlrpc.php', 68494)
(u'/wp-login.php', 1923)
(u'/', 440)
(u'/blog/', 138)
(u'/robots.txt', 123)
(u'/sitemap_index.xml', 118)
(u'/post-sitemap.xml', 118)
(u'/page-sitemap.xml', 117)
(u'/category-sitemap.xml', 117)
(u'/orlando-headlines/', 95)
...

Observe within 2 seconds it is able to analyze the data and still listening if anything comes up
Lets paste like another chunk of data (or copy again same log) you can observe it is changing again


