# Zookeeper

### Go into zookeeper which is by default installed in HDP
[root@sandbox-hdp maria_dev]# cd /usr/hdp/current/zookeeper-client
[root@sandbox-hdp zookeeper-client]# cd bin
[root@sandbox-hdp bin]# ls
zkCleanup.sh  zkServer-initialize.sh  zookeeper-server
zkCli.sh      zkServer.sh             zookeeper-server-cleanup
zkEnv.sh      zookeeper-client        zookeeper-server-initialize

### Open Zookeeper cli
[root@sandbox-hdp bin]# ./zkCli.sh

### To see whats in (preinstalled for Hortonworks HDP sandbox
[zk: localhost:2181(CONNECTED) 1] ls /
[registry, cluster, storm, brokers, zookeeper, infra-solr, hbase-unsecure, admin, isr_change_notification, hiveserver2, controller_epoch, consumers, config]

#### craete a ephimeral node
[zk: localhost:2181(CONNECTED) 2] create -e /testmaster "127.0.0.1:2223"
Created /testmaster

[zk: localhost:2181(CONNECTED) 3] get /testmaster
"127.0.0.1:2223"
cZxid = 0x3ea
ctime = Sun Feb 11 08:01:04 UTC 2018
mZxid = 0x3ea
mtime = Sun Feb 11 08:01:04 UTC 2018
pZxid = 0x3ea
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x1618358f61a000f
dataLength = 16
numChildren = 0

#### when you quit zookeper
[zk: localhost:2181(CONNECTED) 4] quit
It automatically deletes ephimeral nodes 
so, you get like below
[zk: localhost:2181(CONNECTED) 3] get /testmaster                       
Node does not exist: /testmaster

#### create a master again
[zk: localhost:2181(CONNECTED) 4] create -e /testmaster "127.0.0.1:2225"
Created /testmaster
[zk: localhost:2181(CONNECTED) 5] get /testmaster
"127.0.0.1:2225"
cZxid = 0x3ed
ctime = Sun Feb 11 08:04:46 UTC 2018
mZxid = 0x3ed
mtime = Sun Feb 11 08:04:46 UTC 2018
pZxid = 0x3ed
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x1618358f61a0010
dataLength = 16
numChildren = 0

#### when you try to reassign master with same or new
[zk: localhost:2181(CONNECTED) 6] create -e /testmaster "127.0.0.1:2225"
Node already exists: /testmaster

#### zookeper will ensure when master fails , it takes all nodes that compete to become master and ensure only 1 becomes master
