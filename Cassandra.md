# Cassandra
- no single point of failure
- distributed non relational database
- no master node
- NOSQL with a twist
- CQL as its query language and its limited for its non-relational purpose
- Data Model is similar to BigTable/HBase
CAP Theorem says you can have only 2/3 below
-Consistency
-Availability
-Partition Tolerence

Partition Tolerance is requirement with big data. so you can only get to choose 1 among the others
- Cassandra favors Availability over consistency - It will be eventually consistent & really it is tunable consistency
## Cassandra Architecture
- ring structure
- Gossip protocol between all nodes
- replicate the data into another cassandra ring that can be used for analytics and sprak integration
## CQL
- CQL has some limitations
No Joins - your data should be denormalized
all queires must be on primary key
keyspaces are like databases
## spark -cassandra
- datastax provides free spark cassandra connector
- allows you to write , read tables as dataframes
uses:
- use spark for analytics on data stored in cassandra
- use spark to transform the data and store it into cassandra for transactional use

## updating the sandbox
yum update
python -V
yum install
yum install scl-utils
### Horton works sanbox runs on cent-os it needs python2.6 however we need python2.7 for cassandra, so we need something that manage release versions
yum install centos-release-scl-rh
### now install python27
yum install python27
## to switch to python bash
scl enable python27 bash
python -V
## we can't directly install cassandra using yum as hortonworks didn't setup in such a way - there is no cassandra store in it
cd /etc/yum.repos.d
ls
## create a newfile in it for cassandra
vi datastax.repo
``` [datastax]
name = DataStax Repo for Apache Cassandra
baseurl = http://rpm.datastax.com/community
enabled = 1
gpgcheck = 0

```
## to take a peek if the file got it
cat datastax.repo
## now we can install datastax cassandra via yum dsc30 is its package name
yum install dsc30
## we need cql shell to interact in cassandra . lets install that.
pip install cqlsh
## now start the service
service cassandra start
## now open up cqlsh
cqlsh
o/p - ('Unable to connect to any servers', {'127.0.0.1': ProtocolError("cql_version '3.3.1' is not supported by remote (w/ native protocol). Supported versions: [u'3.4.0']",)})
## looks like there is a version mismatch so provide with version flag the necessary version
cqlsh --cqlversion="3.4.0"
## create a keyspace with replication factors & durable_writes. remember keyspace is similar to database
CREATE KEYSPACE movielens WITH replication = {'class':'SimpleStrategy', 'replication_factor':'1'} AND durable_writes = true;
## now use movielens
use MOVIELENS
## create a table
CREATE TABLE users (user_id int, age int, gender text, occupation text, zip text, PRIMARY KEY (user_id));
## describe
DESCRIBE TABLE users;
## SELECT
SELECT * FROM users;

# Cassandra Spark

## first get the script 
wget http://media.sundog-soft.com/hadoop/CassandraSpark.py
## to use data sets we need to use sprak 2.0
export SPARK_MAJOR_VERSION=2
``` python
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def parseInput(line):
    fields = line.split('|')
    return Row(user_id = int(fields[0]), age = int(fields[1]), gender = fields[2], occupation = fields[3], zip = fields[4])

if __name__ == "__main__":
    # Create a SparkSession
    spark = SparkSession.builder.appName("CassandraIntegration").config("spark.cassandra.connection.host", "127.0.0.1").getOrCreate()

    # Get the raw data
    lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/ml-100k/u.user")
    # Convert it to a RDD of Row objects with (userID, age, gender, occupation, zip)
    users = lines.map(parseInput)
    # Convert that to a DataFrame
    usersDataset = spark.createDataFrame(users)

    # Write it into Cassandra
    usersDataset.write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="users", keyspace="movielens")\
        .save()

    # Read it back from Cassandra into a new Dataframe
    readUsers = spark.read\
    .format("org.apache.spark.sql.cassandra")\
    .options(table="users", keyspace="movielens")\
    .load()

    readUsers.createOrReplaceTempView("users")

    sqlDF = spark.sql("SELECT * FROM users WHERE age < 20")
    sqlDF.show()

    # Stop the session
    spark.stop()
    ```
