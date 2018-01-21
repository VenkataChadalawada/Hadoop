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
