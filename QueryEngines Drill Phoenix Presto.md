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

##### Go to hive editor & create database
create database movielens;

##### Now transfer movielens data into MongoDB too using spark
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 MongoSpark.py

#### Download apache drill (find the download mirror tar file link in google & in terminal do wget)
wget http://mirror.stjschools.org/public/apache/drill/drill-1.12.0/apache-drill-1.12.0.tar.gz

#### unzip
tar -xvf apache-drill-1.12.0.tar.gz 

#### starting Drill into another port 
bin/drillbit.sh start -Ddrill.exec.http.port=8765
this opens up Drill on http://localhost:8765/

### go to Query 
show databases;
we have hive.movielens (ratings table as u), mongo.movielens(users table (collection)

#### take a peek onto hive
select * from hive.movielens.u LIMIT 10;

#### take a peel onto mongoDB
select * from mongo.movielens.users LIMIT 10;

#### lets combine - how many ratings break down by occupation
SELECT u.occupation, count( * ) FROM hive.movielens.u r JOIN mongo.movielens.users u ON r.user_id = u.user_id GROUP BY u.occupation

#### stop the drill & mongoDB
bin/drillbit.sh stop
go to Ambari services & stop MongoDB service

## Apache Pheonix
- It mainly works with HBase that supports transactions
- Fast lowlatency - OLTP support
- Originally developed by Salesforce, then opensourced
- Exposes a JDBC connector for HBase - we can also connects to any system using JDBC eg- Tableau
- supports secondary indices and user-defined functions
- Integartes with Mapreduce, Spark, Hive, Pig, and Flume
- Pheonix is really fast. you probably won't pay a performance cost from having this extra layer on top of HBase
- Why Phoenix & not Drill - Choose right tool for the job
- why phoenix and not HBase's native clients? 
  - your apps, and analysts may find SQL easier to work with.
  - Phoenix can do the work of optimizing more complex queries for you
  - But remember HBase is still fundementally non-relational

### Phoenix Architecture
- It has Pheonix Client(parsing, queryplan) on top of HBase API
- Each HBase Region server has an Phoenix Co-Processor attached to it 

### Using Phoenix
- Command Line Interface CLI
- Phoenix APU for Java
- JDBC driver(thick client)
- Phoenix Query Server(PQS) (thin client)
  - Intended to eventually enable non-JVM access
-JAR's for mapReduce, Hive, Pig, Flume, Spark

### Let's play Phoenix
- Install on HDP
- mess arround with the CLI
- set up a users table for Movielens
- store and load data to it through the Pig Integration

#### install using yum
yum install phoenix
- this installs in /usr/hdp/current/phoenix-client/
- ls

#### open up CLI for Phoenix
[root@sandbox-hdp phoenix-client]# cd bin
[root@sandbox-hdp bin]# python sqlline.py

#### List the tables
!tables
0: jdbc:phoenix:> !tables
+------------+--------------+-------------+---------------+----------+------------+----------------------------+---------+
| TABLE_CAT  | TABLE_SCHEM  | TABLE_NAME  |  TABLE_TYPE   | REMARKS  | TYPE_NAME  | SELF_REFERENCING_COL_NAME  | REF_GEN |
+------------+--------------+-------------+---------------+----------+------------+----------------------------+---------+
|            | SYSTEM       | CATALOG     | SYSTEM TABLE  |          |            |                            |         |
|            | SYSTEM       | FUNCTION    | SYSTEM TABLE  |          |            |                            |         |
|            | SYSTEM       | SEQUENCE    | SYSTEM TABLE  |          |            |                            |         |
|            | SYSTEM       | STATS       | SYSTEM TABLE  |          |            |                            |         |
+------------+--------------+-------------+---------------+----------+------------+----------------------------+---------+
0: jdbc:phoenix:> 

#### creating a table & putting a compound key on it
CREATE TABLE IF NOT EXISTS us_population ( state CHAR(2) NOT NULL, city VARCHAR NOT NULL, population BIGINT CONSTRAINT my_pk PRIMARY KEY (state, city));
0: jdbc:phoenix:> CREATE TABLE IF NOT EXISTS us_population ( state CHAR(2) NOT NULL, city VARCHAR NOT NULL, population BIGINT CONSTRAINT my_pk PRIMARY KEY (state, city));
No rows affected (1.31 seconds)
0: jdbc:phoenix:> !tables
+------------+--------------+----------------+---------------+----------+------------+----------------------------+------+
| TABLE_CAT  | TABLE_SCHEM  |   TABLE_NAME   |  TABLE_TYPE   | REMARKS  | TYPE_NAME  | SELF_REFERENCING_COL_NAME  | REF_ |
+------------+--------------+----------------+---------------+----------+------------+----------------------------+------+
|            | SYSTEM       | CATALOG        | SYSTEM TABLE  |          |            |                            |      |
|            | SYSTEM       | FUNCTION       | SYSTEM TABLE  |          |            |                            |      |
|            | SYSTEM       | SEQUENCE       | SYSTEM TABLE  |          |            |                            |      |
|            | SYSTEM       | STATS          | SYSTEM TABLE  |          |            |                            |      |
|            |              | US_POPULATION  | TABLE         |          |            |                            |      |
+------------+--------------+----------------+---------------+----------+------------+----------------------------+------+
0: jdbc:phoenix:> 
#### insert data into Phoenix 
note - no INSERT in Phoenix , it has UPSERT
UPSERT INTO US_POPULATION VALUES ('NY', 'New York', 8143197);
UPSERT INTO US_POPULATION VALUES ('CA', 'Los Angeles', 3843197);

#### view tables
SELECT * FROM US_POPULATION;

SELECT * FROM US_POPULATION WHERE STATE='CA';
+--------+--------------+-------------+
| STATE  |     CITY     | POPULATION  |
+--------+--------------+-------------+
| CA     | Los Angeles  | 3843197     |
+--------+--------------+-------------+
1 row selected (0.071 seconds)
0: jdbc:phoenix:> 

#### delete table us_population
DROP TABLE US_POPULATION

#### quit
!quit


### Use movie lens's user table - write a pig script that uses phoenix to write and store users data table(relation in pig) into HBase via Phoenix and read it back and do queries on it phoenix
cd into /usr/hdp/current/phoenix-client/bin
##### open up the cli & create a table first
python sqlline.py

REATE TABLE users ( USERID INTEGER NOT NULL, AGE INTEGER, GENDER CHAR(1), OCCUPATION VARCHAR, ZIP VARCHAR CONSTRAINT pk PRIMARY KEY (USERID));
No rows affected (2.39 seconds)
0: jdbc:phoenix:> ! tables
+------------+--------------+-------------+---------------+----------+------------+----------------------------+---------+
| TABLE_CAT  | TABLE_SCHEM  | TABLE_NAME  |  TABLE_TYPE   | REMARKS  | TYPE_NAME  | SELF_REFERENCING_COL_NAME  | REF_GEN |
+------------+--------------+-------------+---------------+----------+------------+----------------------------+---------+
|            | SYSTEM       | CATALOG     | SYSTEM TABLE  |          |            |                            |         |
|            | SYSTEM       | FUNCTION    | SYSTEM TABLE  |          |            |                            |         |
|            | SYSTEM       | SEQUENCE    | SYSTEM TABLE  |          |            |                            |         |
|            | SYSTEM       | STATS       | SYSTEM TABLE  |          |            |                            |         |
|            |              | USERS       | TABLE         |          |            |                            |         |
+------------+--------------+-------------+---------------+----------+------------+----------------------------+---------+
0: jdbc:phoenix:> 
 ##### quit 
 ! quit
 
 ##### check if you have ml-100k in home directory
 cd /home/maria_dev
 
 ##### get the pig script
 wget https://media.sundog-soft.com/hadoop/phoenix.pig

##### script
``` python
REGISTER /usr/hdp/current/phoenix-client/phoenix-client.jar

users = LOAD '/user/maria_dev/ml-100k/u.user'
USING PigStorage('|')
AS (USERID:int, AGE:int, GENDER:chararray, OCCUPATION:chararray, ZIP:chararray);

STORE users into 'hbase://users' using
    org.apache.phoenix.pig.PhoenixHBaseStorage('localhost','-batchSize 5000');

occupations = load 'hbase://table/users/USERID,OCCUPATION' using org.apache.phoenix.pig.PhoenixHBaseLoader('localhost');

grpd = GROUP occupations BY OCCUPATION;
cnt = FOREACH grpd GENERATE group AS OCCUPATION,COUNT(occupations);
DUMP cnt;

```
Thus, We have stored users data from movielens into HBase through Phoenix

Load back the userid, occupation from users table in Hbase using pig.PhoenixHBaseLoader connector class which makes pig talk to Phoenix
#### Run it in Pig
pig phoenix.pig 

cd /usr/hdp/current/phoenix-client/bin

python sqlline.py

!table

SELECT * FROM users LIMIT 10;

DROP TABLE users;

!tables

!quit

## PRESTO
### what is Presto
- It can connect to many different BigData databases and data stores at once and query across them
- Familiar SQL syntax
- notonly a database itself - works like a layer
- its like Drill
- Optimized for OLAP- analytical queries, data warehousing
- Developed and still partially maintained by Facebook
- Developed, and still partially maintained by Facebook
- Exposes JDBC, CommandLine and Tableau
### Why Presto?
Vs Drill? It has Cassandra connector for one thing
If it is good enough for Facebook
Facebok uses Presto for interactie queries against several internal data stores, including their 300PB data warehouse. Over 1000 Facebook employees use Presto daily to run more than 30000 queries that in total scan over a petabyte each per day
- Also used by DropBox and AirBNB
- A single Presto query can combine data from multiple sources, allowing for analytics across your entire organization"
Presto Breaks the false choice between having fast analytics using an expensive commerical solution that requires excessive hardware

what can presto connect to?
- cassandra (It's Facebook, afterall)
- Hive
- MongoDB
- MySQL
- Local files
- and stuff like Kafka, JMX, PostgreSql, Redis, Accumulo

### Lets just dive in
- Set up Presto
- Query our Hive ratings table using Presto
- Spin Cassandra up, and query our table in Cassandra with presto
- Execute a query that joins users in Cassandra with ratings in Hive!

## Installation Presto
go presto site copy the tar ball link
& go to our terminal sandbox and do wget
https://prestodb.io/docs/current/installation/deployment.html
wget https://repo1.maven.org/maven2/com/facebook/presto/presto-server/0.193/presto-server-0.193.tar.gz
#### untar example
tar -xvf presto-server-0.194.tar.gz
cd presto-server-0.194
#### Set up presto config
// he already did enough config for the sandbox which you can download
wget http://media.sundog-soft.com/hadoop/presto-hdp-config.tgz
tar -xvf presto-hdp-config.tgz
#### if you wanna take a peek on those files
cd etc
vi config.properties 
vi node.properties 
cd catalog/
vi hive.properties 
cd.. cd..
[root@sandbox-hdp bin]# pwd
/home/maria_dev/presto-server-0.194/bin
[root@sandbox-hdp bin]# mv presto-cli-0.194-executable.jar presto
#### changing into exectuable mode
chmod +x presto
#### start here & check web interface
[root@sandbox-hdp presto-server-0.194]# pwd
/home/maria_dev/presto-server-0.194
[root@sandbox-hdp presto-server-0.194]# bin/launcher start
Started as 10039
[root@sandbox-hdp presto-server-0.194]# 
Now it will open up in http://localhost:8090/

#### Open presto cli in terminal
[root@sandbox-hdp presto-server-0.194]# bin/presto --server 127.0.0.1:8090 --catalog hive
presto> 


cd etc

