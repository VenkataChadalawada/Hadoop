# Streaming with kafka
- Kafka is a general-purpose publish/subscribe messaging system
- Kafka servers store all incomming messages from publishers for some period of time and publishes them to a stream of data called a topic
- Kafka consumers subscribe to one or more topics and receive data as it's published
- A stream/topic can have many different consumers, all with their own position in the stream maintained
- Its not just for Hadoop

## Kafka architecture check out notes
## How Kafka Scales
It can be a cluster of its own
- Kafka itself may be distributed among many processes on many servers
- will distribute the storage of stream data as well
- consumers amy also be distributed
- consumers of the same group will have messages distributed amongst them
- consumers of different groups will get their own copy of each message

## let's play
Start Kafka on our sandbox
set up a topic
- publish some data to it and watch it get consumed
- set up a file connector & monitor a log file and publish additions to it

## Start
go to ambari -> click Kafka -> servic actions start
Now login via termina
ssh maria_dev@127.0.0.1 -p2222
 
## Go to kafka
[maria_dev@sandbox-hdp ~]$ cd /usr/hdp/current/kafka-broker/
//here is where it lives
cd bin

## create a kafka topic & track that with zookeeper                                                    
[maria_dev@sandbox-hdp bin]$ ./kafka-topics.sh --create --zookeeper sandbox.hortonworks.com:2181 --replication-factor 1 --partitions 1 --topic venkata
Created topic "venkata".

## list the topics to see whether venkata is among them
[maria_dev@sandbox-hdp bin]$ ./kafka-topics.sh --list --zookeeper sandbox.hortonworks.com:2181
ATLAS_ENTITIES
ATLAS_HOOK
__consumer_offsets
venkata

## lets publish some data into it
//sample producer app that talks to kafka & produces data into kafka
- [maria_dev@sandbox-hdp bin]$ ./kafka-console-producer.sh --broker-list sandbox.hortonworks.com:6667 --topic venkata

where:
--broker-list - specifies the kafka server itself
so what it does is it listens anything on venkata

### Lets consume via consumers
- open up another terminal , cd /usr/hdp/current/kafka-broker/bin
- ./kafka-console-consumer.sh --bootstrap-server sandbox.hortonworks.com:6667 --zookeeper localhost:2181 --topic venkata --from-beginning

--from-beginning gives all the data from beginning





