# Zeppelin
- Quick way to visualize bigdata on your Apache Spark Scripts
It also have plugins for HBase, Hive Pig etc..
- Tool to do Data Science in BigData
- If you're familiar with ipython notebooks - its like that
- can interleave with nicely formatted notes
- can share notebooks with others on your cluster
- If you're familiar with ipython notebook - well, you kind of just have to see it
- Can run Code interactively ( like you can in the spark shell)
- This speeds up your development cycle
- And allows easy experimentation and exploration
- Can execute SQL queries directly against SparkSQL
- Query results may be visualized in charts and graphs
- makes Spark feel more like a data science tool.

## It can be integrated with
- Alluxio
- Google BigQuery
- Cassandra 
- elasticSearch
- Flink
- Apache Geode
- Apache HBase
- Hadoop hdfs
- Hive
- Apache Ignite
- Lens
- Livy
- PostgresSQL
- python
- R
- Scalding
- Tajo

### Opening Zepplin
By default sandbox opens it at 9995 port
localhost:9995/

### click create a new notebook %md is mark down (similar to git .md)
%md
``` python
### Let's make sure spark is working first!
Let's see what version it has got
```
o/p
### Let’s make sure Spark is working first
Let’s see what version we are

FINISHED   
Took 2 sec. Last updated by anonymous at February 11 2018, 5:34:47 AM.
// find the version
sc.version
o/p:
res0: String = 2.2.0.2.6.3.0-235
FINISHED   
Took 44 sec. Last updated by anonymous at February 11 2018, 5:38:48 AM.

### shell commands (lets write Spark in Scala)
%sh
wget http://media.sundog-soft.com/hadoop/ml-100k/u.data -O /tmp/u.data
wget http://media.sundog-soft.com/hadoop/ml-100k/u.item -O /tmp/u.item
echo "Downloaded!"
(get the data & output that to tmp folder


### Now copy that from tmp into HDFS
//first if any directory exist recursively delete with force
%sh
hadoop fs -rm -r -f /tmp/ml-100k
//create a directory in HDFS
hadoop fs -mkdir /tmp/ml-100k
// copy this local data into HDFS data
hadoop fs -put /tmp/u.data /tmp/ml-100k/
hadoop fs -put /tmp/u.item /tmp/ml-100k/

### you can give a title to each print in Zeppelin
click right gear icon & title

### spark in scala
//class object of Rating which contains movieID of Int & Rating of Int
final case class Rating(movieID: Int, rating: Int)
val lines = sc.textFile("hdfs://tmp/ml-100k/u.data").map(x => {val fields = x.split("\t"); Rating(fields(1).toInt, fields(2).toInt)})

### converting into dataframe
import sqlContext.implicits._
val ratingsDF = lines.toDF()
ratingsDF.printSchema()

### groupby movieID's count in descending order
val topMovieIDs = ratingsDF.groupBy("movieID").count().orderBy(desc("count")).cache()
topMovieIDs.show()

topMovieIDs: org.apache.spark.sql.Dataset[org.apache.spark.sql.Row] = [movieID: int, count: bigint]
+-------+-----+
|movieID|count|
+-------+-----+
|     50|  584|
|    258|  509|
|    100|  508|
|    181|  507|
|    294|  485|
|    286|  481|
|    288|  478|
|      1|  452|
|    300|  431|
|    121|  429|
|    174|  420|
|    127|  413|
|     56|  394|
|      7|  392|
|     98|  390|
|    237|  384|
|    117|  378|
|    172|  368|
|    222|  365|
|    204|  350|
+-------+-----+
only showing top 20 rows

### lets do something in SQL now in Zeppelin - now our spark dataframe just behaves like a sql table
ratingsDF.registerTempTable("ratings")
%sql
SELECT * FROM RATINGS LIMIT 10

%sql
SELECT rating, COUNT( * ) AS count FROM RATINGS GROUP BY rating

### get back to spark sacala
final case class Movie(movieID:Int, title:String)
val lines = sc.textFile("hdfs:///tmp/ml-100k/u.item").map(x => {val fields = x.split('|'); Movie(fields(0).toInt, fields(1))})

import sqlContext.implicits._
val moviesDF = lines.toDF()
moviesDF.show()


%sql
SELECT t.title, count(*) AS cnt FROM ratings r JOIN titles t ON r.movieID = t.movieID GROUP BY t.title ORDER BY cnt DESC LIMIT 20
