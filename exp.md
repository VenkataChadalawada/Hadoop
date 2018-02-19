
- hands on with Hortonworks sandbox
- worked on Ambari interface
- wrote mapreduce programs in python
- Good understanding on YARN
- experienced in writing pig scripts in piglatin
- executed hive queries on Ambari hive interface
- created spark program to extract toprated movies & least ranked movies in both Spark & Spark 2.0
- defined RDD's & data frames in spark to retrive spark's internal Directed Acyclic Graphs.
- done partitions of data from single source using partion in hive
- wrote joins in hive to combine views and tables to bring the final result
- creating tables in mysql writing complex queries with joins groups in mysql
- importing mysql tables into hdfs and hive using sqoop
- exporting tables from hdfs to mysql using sqoop
- runing hbase server and connecting to it through python client & importing data into Hbase via starbase & portforwarding
- interacting through Hbase shell and creating tables, scanning, dropping
- using pig to import data into HBase using pig.backend.hadoop.hbase.HBaseStorage
- Installing Datastax Cassandra in the hortonworks centos sandbox and cqlsh for shell interaction
- Cassandra - wrting CQL commands, creating keyspaces and tables
- performing analytics using spark in cassandra
- creating a spark session, getting the raw data converting that to a DataFrame and writing it into Cassandra
- Reading it back from cassandra into a new dataframe 
- copy of users DB into a spark dataframe from movielens data set into MongoDB
- Did some aggregations on Mongo DB like creating a DB , creating group avg calculations
- finding the records in mongoDB by creating Indexes
- picking right database for the requirement how to pick MongoDB vs Cassandra

Query Engines
- configure Drill & establish a port in HDP
- interact with data in Hive , mongoDB in HDP via Drill
- Write joins across the data bases in hadoop echosystem to get the count & group by data
- Install Phoenix & create tables using its python based CLI
- creating tables & applying a compound key, Inserting data, view , delete tables in Pheonix
- write a pig script that uses phoenix to write and store users data table(relation in pig) into HBase via Phoenix and read it back and do queries on it phoenix
- Set up Presto
- Query our Hive ratings table using Presto
- Spin Cassandra up, and query our table in Cassandra with presto
- Execute a query that joins users in Cassandra with ratings in Hive!

- hands on with zookeeper
- setting up a Oozie workflow that gets data from mysql & puts into Hive
- creating a new notebook with spark in zeppelin
- Adjusting the priority order with spark as top in Zeppelin
- dowloading raw data into sandbox & executing hadoop -put to move the data into HDFS
- writing spark in scala to analyze the data by creating classes & dataframes executed in shell comands
- exposed spark dataframes as sql tables & analyzed some queries
- joins groups orders of the data sets and visualize them in barcharts pie charts line graphs in Zeppelin

Streaming
Kafka
- creating a producer & consumer kafka flow with a topic.
Flume
- Construct a Flume agent which has source:netCat , Channel :memory, Sink:Logger
- Log spool to HDFS = Spool real log files , setup SpoolDir source that monitors a directory for new files dropped into it, built a timestamp interceptor
insert a header to address what time it logged in, then push through a memory channel got to a HDFS sink, not only write data but structure hiararchy year month date

Analyzing Streams
SparkStreaming
- set up Flume to use a spooldir source, use an Avro Sink to connect through our spark streaming job 
- use a window to aggregate how often each url appears from the access logs

