# Query Engines
- Drill - issues SQL queries across wide range of upon your hadoop system HDFS, Google Cloude Storeage , Microsoft Azure or S3 .It can't talk to Cassandra but can also talk to Mongo
- Hue
- Phoenix - on top of HBase - issue SQL queries that aren't really a relational DB's
- Presto - lot like Drill, Its made by Facebook It can talk to cassandra but not mongoDB
- Apache Zeppelin

## Apache Drill
A SQL query engine for a variety of non-relational databases and datafiles
- Hive, MongoDB, HBase
- Even flat JSON or Parquet files on HDFS, S3, Azure, Google Cloud, local file system
- Based on Google's Dremel
- Its actual SQL - so you can write any SQL query
- Drill can also pose like a relational DB , so that you can connect to Tableau etc
- Internally data is represented as JSON and so has no fixed schema
- Allows SQL analysis of disparate data source without having to transform and load it first
- drill.apache.org 
- you can join between sources ex: join between mongoDB Hive and some S3(Amazon)

### Let's Drill
We will import data into Hive & MongoDB
Set up Drill on top of both
and do some queries

- Go to hive editor & create database
create database movielens;

- Now transfer movielens data into MongoDB too using spark


