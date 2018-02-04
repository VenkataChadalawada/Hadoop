# Design Considerations
- what systems you need to integrate together?
- Diff tech have diff connectors
  for eg- analytics job is currently running in Apache spark then you might limit ext DB's that work along with spark
- may be frontend systems SQL to Backend thinking of moving RDBMS to NoSQL - maybe HiveQL for ease
- scaling requirements
- support considerations (security)
- Budget considerations
- Keep it simple
- 
## Example which DB to pick
Q) Building a massive stock trading system - so consistency is very imp
Big Data is present
Its imp to have some security & access to professional support might be a good idea and you have enough budget to pay for it


CAP theorem

Availability
             
consistency

Partition Tolerance

Availability + Consistency => MySQL etc..
Availability + Partition Tolerance => Cassandra etc..
Consistency + Partition Tolerance => HBase, MongoDB etc..

MongoDB & HBase are good choice . MongoDB has good professional support

We can have some configuration to use Cassandra & it has good support too

