# MongoDB 
- Came from word huMANGOus data
- Document based data model
- looks like JSON
- no real schema is enforced
- no single key like in other databses
- It is NOSQL so no Joins

## Terminology:
- DataBases
- Collections  ~ similar to Tables
- Documents  ~ similar to rows

## Replication Sets
- Single master
- Maintains backup copies of your database instances
- secondaries can elect a new primary within seconds if your primary goes down
- But make sure your operation log is long enough to give you time to recover the primary when it comes back..

- A majority  of servers in your set must agree on primary
- even numbers dont work so you might need to set up an arbitary in such cases
- Apps must know about enough servers in the replica set to be ables to reach one to learn who's primary
- Replicas only address durability, not your ability to scale
- your DB will still go into read-only mode for a bit while new primary is elected
- Delayed secondaries can be set up as insurance against people doing dumb things

### Sharding
- multiple replica sets.

### Architecture with Big data
AppServerProcess > Mongos talks to > config servers (3) > and decides which primary node & get the data from secondaries respectively.
Mongos also runs a balancer incase selected primary secondaries missed something It can fetch it from others
for eg:- Replica Set1 (RS1) is handling min to 1000 
and replica set 2 (RS2) is handling 1000 to 5000
& replica set 3 (RS3) is handling 5000 to max
It can change over time & rebalanced over time as the need arises

### Sharding quirks (disadvantages)
- Auto-Sharding sometimes doesn't work - split storms, mongo processes restarted soon
- you must have 3 config servers - if anyone goes down - your DB is down

### Advantages
- Shell is a full javascript interpreter
- very flexible document model compared to a NoSQL databases in general
- supports many indices but only one can be used for sharding, more than 2-3 are still discouraged, full-test indices for text searches, spatial indices
- Builtin aggregation capabilities, MapReduce, gridFS - FOr some applications you might not need hadoop at all
- But MongoDB still integrates with Hadoop Spark & most languages
- An SQL connector is avlbl but remember Mongo is still isn't designed for joins and normalized data really

## Install MongoDB in Ambari
#### connect to terminal as root into Ambari
cd /var/lib/ambari-server/resources/stacks/HDP/2.6
#### git clone a connector
git clone https://github.com/nikunjness/mongo-ambari.git
#### restart Ambari
sudo service ambari restart

### Now you have MongoDB in the sandbox
- Login to sandbox as root
ssh maria_dev@127.0.0.1 -p2222
maria_dev

su root
A*** 3

- Install pymongo to interact in python
pip install pymongo

#### Let's add some data into MongoDB using spark dataframe
- get the script
wget http://media.sundog-soft.com/hadoop/MongoSpark.py
- use spark 2 as we have both in the sandbox
export SPARK_MAJOR_VERSION=2

-know the spark & scala version that your HDP has by opening spark-shell
spark-shell
// mine is spark 2.2.0  scala in it - 2.11.8.

- now submit the script to spark using the mongo-spark connector
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 MongoSpark.py
``` python
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def parseInput(line):
    fields = line.split('|')
    return Row(user_id = int(fields[0]), age = int(fields[1]), gender = fields[2], occupation = fields[3], zip = fields[4])

if __name__ == "__main__":
    # Create a SparkSession
    spark = SparkSession.builder.appName("MongoDBIntegration").getOrCreate()

    # Get the raw data
    lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/ml-100k/u.user")
    # Convert it to a RDD of Row objects with (userID, age, gender, occupation, zip)
    users = lines.map(parseInput)
    # Convert that to a DataFrame
    usersDataset = spark.createDataFrame(users)

    # Write it into MongoDB
    usersDataset.write\
        .format("com.mongodb.spark.sql.DefaultSource")\
        .option("uri","mongodb://127.0.0.1/movielens.users")\
        .mode('append')\
        .save()

    # Read it back from MongoDB into a new Dataframe
    readUsers = spark.read\
    .format("com.mongodb.spark.sql.DefaultSource")\
    .option("uri","mongodb://127.0.0.1/movielens.users")\
    .load()

    readUsers.createOrReplaceTempView("users")

    sqlDF = spark.sql("SELECT * FROM users WHERE age < 20")
    sqlDF.show()

    # Stop the session
    spark.stop()
```
It generates table like below:

+--------------------+---+------+----------+-------+-----+                      
|                 _id|age|gender|occupation|user_id|  zip|
+--------------------+---+------+----------+-------+-----+
|[5a671e6b46e0fb7c...| 18|     F|   student|    482|40256|
|[5a671e6b46e0fb7c...| 18|     F|    writer|    507|28450|
|[5a671e6b46e0fb7c...| 19|     M|   student|    521|02146|
|[5a671e6b46e0fb7c...| 18|     M|   student|    528|55104|
|[5a671e6b46e0fb7c...| 19|     F|   student|    541|84302|
|[5a671e6b46e0fb7c...| 16|     F|   student|    550|95453|
|[5a671e6b46e0fb7c...| 16|     M|   student|    580|17961|
|[5a671e6b46e0fb7c...| 17|     M|   student|    582|93003|
|[5a671e6b46e0fb7c...| 18|     F|   student|    588|93063|
|[5a671e6b46e0fb7c...| 18|     M|   student|    592|97520|]

### getting into MongoDB shell
- open the mongo shell
mongo
- use/create a database
> use movielens;
switched to db movielens
> db.users.find({user_id:100})
{ "_id" : ObjectId("5a671e6b46e0fb7c9479ed93"), "age" : NumberLong(36), "gender" : "M", "occupation" : "executive", "user_id" : NumberLong(100), "zip" : "90254" }

- To see the execution plan under finding the userid
>db.users.explain().find({user_id:100})
o/p
``` javascript
{
	"queryPlanner" : {
		"plannerVersion" : 1,
		"namespace" : "movielens.users",
		"indexFilterSet" : false,
		"parsedQuery" : {
			"user_id" : {
				"$eq" : 100
			}
		},
		"winningPlan" : {
			"stage" : "COLLSCAN",
			"filter" : {
				"user_id" : {
					"$eq" : 100
				}
			},
			"direction" : "forward"
		},
		"rejectedPlans" : [ ]
	},
	"serverInfo" : {
		"host" : "sandbox-hdp.hortonworks.com",
		"port" : 27017,
		"version" : "3.2.18",
		"gitVersion" : "4c1bae566c0c00f996a2feb16febf84936ecaf6f"
	},
	"ok" : 1
}
```
- if you see its winningPlan is a scan forward until it finds 100 id. which is not a good plan. so lets set an index.

db.users.createIndex({user_id:1})
{
	"createdCollectionAutomatically" : false,
	"numIndexesBefore" : 1,
	"numIndexesAfter" : 2,
	"ok" : 1
}
- Now lets find with explain and check the winning plan
db.users.explain().find({user_id:100})
{
	"queryPlanner" : {
		"plannerVersion" : 1,
		"namespace" : "movielens.users",
		"indexFilterSet" : false,
		"parsedQuery" : {
			"user_id" : {
				"$eq" : 100
			}
		},
		"winningPlan" : {
			"stage" : "FETCH",
			"inputStage" : {
				"stage" : "IXSCAN",
				"keyPattern" : {
					"user_id" : 1
				},
				"indexName" : "user_id_1",
				"isMultiKey" : false,
				"isUnique" : false,
				"isSparse" : false,
				"isPartial" : false,
				"indexVersion" : 1,
				"direction" : "forward",
				"indexBounds" : {
					"user_id" : [
						"[100.0, 100.0]"
					]
				}
			}
		},
		"rejectedPlans" : [ ]
	},
	"serverInfo" : {
		"host" : "sandbox-hdp.hortonworks.com",
		"port" : 27017,
		"version" : "3.2.18",
		"gitVersion" : "4c1bae566c0c00f996a2feb16febf84936ecaf6f"
	},
	"ok" : 1
}

- Thats an example of how to set Index in MongoDB. So MongoDB doesn't do automatically - we have to set up Indexes otherwise its gonna be hardly ineffcient.
db.users.find({user_id:100})
{ "_id" : ObjectId("5a671e6b46e0fb7c9479ed93"), "age" : NumberLong(36), "gender" : "M", "occupation" : "executive", "user_id" : NumberLong(100), "zip" : "90254" }

MongoDB finding avgAge
``` javascript
db.users.aggregate([ { $group: { _id:{occupation: "$occupation"}, avgAge: { $avg: "$age"}}} ])
{ "_id" : { "occupation" : "doctor" }, "avgAge" : 43.57142857142857 }
{ "_id" : { "occupation" : "healthcare" }, "avgAge" : 41.5625 }
{ "_id" : { "occupation" : "none" }, "avgAge" : 26.555555555555557 }
{ "_id" : { "occupation" : "engineer" }, "avgAge" : 36.38805970149254 }
{ "_id" : { "occupation" : "homemaker" }, "avgAge" : 32.57142857142857 }
{ "_id" : { "occupation" : "marketing" }, "avgAge" : 37.61538461538461 }
{ "_id" : { "occupation" : "artist" }, "avgAge" : 31.392857142857142 }
{ "_id" : { "occupation" : "librarian" }, "avgAge" : 40 }
{ "_id" : { "occupation" : "entertainment" }, "avgAge" : 29.22222222222222 }
{ "_id" : { "occupation" : "scientist" }, "avgAge" : 35.54838709677419 }
{ "_id" : { "occupation" : "salesman" }, "avgAge" : 35.666666666666664 }
{ "_id" : { "occupation" : "educator" }, "avgAge" : 42.01052631578948 }
{ "_id" : { "occupation" : "lawyer" }, "avgAge" : 36.75 }
{ "_id" : { "occupation" : "student" }, "avgAge" : 22.081632653061224 }
{ "_id" : { "occupation" : "programmer" }, "avgAge" : 33.121212121212125 }
{ "_id" : { "occupation" : "administrator" }, "avgAge" : 38.74683544303797 }
{ "_id" : { "occupation" : "writer" }, "avgAge" : 36.31111111111111 }
{ "_id" : { "occupation" : "retired" }, "avgAge" : 63.07142857142857 }
{ "_id" : { "occupation" : "executive" }, "avgAge" : 38.71875 }
{ "_id" : { "occupation" : "other" }, "avgAge" : 34.523809523809526 }
Type "it" for more

```
- To get the count in Mongo DB 
db.users.count()
943
- see the coolections
b.getCollectionInfos()
[ { "name" : "users", "options" : { } } ]

- Deleting the database
> db.users.drop()
true
> db.getCollectionInfos()
[ ]
- exit mongo
exit

> 
