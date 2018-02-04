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





