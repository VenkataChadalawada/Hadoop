# Flume
Similar to Kafka, Another way to to do streaming data into your cluster
- made from the start with Hadoop in mind
- originally made to handle the problem of log aggregation

## Anatomy of Flume Agents
Webservers -> source -> channel -> sink -> HBase

## Components
#### Sources
- where the data is comming from
- can optionally have channel selectors and Interceptors
#### Channels
- How the data is transfered (via memory or files)
#### Sink
- where the data is going
- Can be organized into sink groups
- A sink can connect to only one channel
- channel is notified to delete a message once the sink processes it.
## Built in Source Types
- Spooling directory
- Avro
- Kafka
- Exec
- Thrift
- Netcat
- Http
- Custom
- And More!
## Using Avro agents can connect to another agents as well
Appservers -->flume agents (Avro Sink) ->(Avro Source)ultimate final flume agent (Avro Sink) --> (Avro Source) HDFS /something

## Let's play
- 1. Construct a Fluem agent which has source:netCat , Channel :memory, Sink:Logger
- 2. Log spool to HDFS = Spool real log files , setup SpoolDir source that monitors a directory for new files dropped into it, built a timestamp interceptor
insert a header to address what time it logged in, then push through a memory channel got to a HDFS sink, not only write data but structure hiararchy year month date

## Exercide 1
### need config files
Download from prof website: wget media.sundog-soft.com/hadoop/example.conf

``` javascript
# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = netcat
a1.sources.r1.bind = localhost
a1.sources.r1.port = 44444

# Describe the sink
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
``` 
## open another terminal
[maria_dev@sandbox-hdp ~]$ cd /usr/hdp/current/flume-server/
[maria_dev@sandbox-hdp flume-server]$ bin/flume-ng agent --conf conf --conf-file ~/example.conf --name a1 -Dflume.root.logger=INFO,console

So, in the first terminal now do a telnet & send something to that terminal which has flume running with our configuration
[maria_dev@sandbox-hdp ~]$ telnet localhost 44444
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Hello there how are you
OK

Now you see that coming in that terminal
2018-02-18 19:30:53,629 (SinkRunner-PollingRunner-DefaultSinkProcessor) [INFO - org.apache.flume.sink.LoggerSink.process(LoggerSink.java:70)] Event: { headers:{} body: 48 65 6C 6C 6F 20 74 68 65 72 65 20 68 6F 77 20 Hello there how  }

#### quit
control+D 

## Exercice 2
http://media.sundog-soft.com/hadoop/flumelogs.conf
``` configuration
# flumelogs.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = spooldir
a1.sources.r1.spoolDir = /home/maria_dev/spool
a1.sources.r1.fileHeader = true
a1.sources.r1.interceptors = timestampInterceptor
a1.sources.r1.interceptors.timestampInterceptor.type = timestamp

# Describe the sink
a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = /user/maria_dev/flume/%y-%m-%d/%H%M/%S
a1.sinks.k1.hdfs.filePrefix = events-
a1.sinks.k1.hdfs.round = true
a1.sinks.k1.hdfs.roundValue = 10
a1.sinks.k1.hdfs.roundUnit = minute

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1

```
### create directories we gonna be using
I'm in home maria dev
mkdir spool
[maria_dev@sandbox-hdp ~]$ mkdir spool
[maria_dev@sandbox-hdp ~]$ ls
CassandraSpark.py  job.properties       presto-server-0.194.tar.gz  u.data
example.conf       ml-100k              spark-warehouse             u.data.1
flumelogs.conf     presto-server-0.194  spool

We also gonna setup our folder on HDFS that things gonna go into
Login to Ambari -> filesview
goto user/maria_dev create a new folder "flume"

### now run flume with this new conf above from flume-server dir
[maria_dev@sandbox-hdp flume-server]$ bin/flume-ng agent --conf conf --conf-file ~/flumelogs.conf --name a1 -Dflume.root.logger=INFO,console

### download some logs & copy that into our spool dir
 wget http://media.sundog-soft.com/hadoop/access_log_small.txt
[maria_dev@sandbox-hdp ~]$ cp access_log_small.txt spool/venkata_logs.txt
[maria_dev@sandbox-hdp ~]$ cd spool/
[maria_dev@sandbox-hdp spool]$ ls
venkata_logs.txt.COMPLETED
- notice that Flume has processed that and appended .COMPLETED to it.

### now observe output data in Ambari usr/maria_dev/flume in our config sepcified way
:) That's flume

Now how to process this streaming data ? = Spark Streaming / Apache Storm/ Flink


