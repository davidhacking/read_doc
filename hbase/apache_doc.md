# 拼多多放羊记
- hbae是什么：Sparse(稀疏存储的), Consistent, Distributed, Multidimensional, Sorted map.
### [Physical View](http://hbase.apache.org/0.94/book/physical.view.html)
- 从概念上hbase是一个存储一行一行记录的东西，物理上是按照每个col family存储的。
- 存储是按照timestamp的降序排列的，如果在某个col上是没有值而在同一行的另一个col上是有值的则不会存储没指的那个cell，所以我想其实hbase存储是使用用户的rowkey加上timestamp存储的。
- row的存储是按照字典升序排列的
- column family需要使用可printable的字母表示，而qualifier不需要只需要byte就行了，而且qualifier可以在需要的时候就增加，即时table is enable
- 由于一个column family的tunings and storage的声明在定义的时候就已经完成了，而且一个column family的数据都存储在一起，所以最好一个column family的数据都是格式一样的较好
- puts 的执行如果通过HTable.put则会通过writeBuffer的方式进行，如果HTable.batch则通过non-writeBuffer的方式进行
	- writeBuffer是客户端缓存，用来提供hbase性能的，因为一次写操作其实包含3部分的时间
		- T1 RTT round trip time 客户端发起传输到服务器确认时间
		- T2 put数据网络传输耗时
		- T3 服务器处理时间
	- 设置writeBuffer是用风险的，因为这些数据没有写到WAL上，数据是容易丢失的
	- 每次的put操作实际是hbase client自己计算应该push到那个region server上的[link](http://www.cnblogs.com/panfeng412/archive/2012/10/16/how-to-use-hbase-client-write-buffer.html)
- scan是通过生命keystart和keyend的方式进行scan的
- delete操作在做的时候并不会真正的delete values，之后标记一个墓碑tombstones，values的删除会在一次[major compactions](http://hbase.apache.org/0.94/book/regions.arch.html#compaction)中彻底删除
### [versions](http://hbase.apache.org/0.94/book/versions.html)
- version: milliseconds
- 使用get操作得到的cell是最大的version，但是可能不是最近一个写的记录
- put操作即可以显式的set version，也可以让hbase做set version操作，version有一个ttl清除机制。建议不用timestamp做自己的业务逻辑相关的操作，可以使用而外的字段或则在rowkey中使用timestamp字段
- delete操作默认删除比指定的时间戳更小的所有记录，如果KEEP_DELETED_CELLS这个属性在column family上设置了那么所有被标记成墓碑的记录不会在major compactions中清除，set ttl hbase.hstore.time.to.purge.deletes
- <span style="color:red;">delete的坑</span>, 只能说一点6，如果你删除了一坨记录timestamp<=T，然后很开心的插入一些记录timestamp<=T，好了这个时候并不能get这些记录出来，但是当那些tombstones记录被删了就可以了get了。。，versions这一节可以好好看看，这个page的outer link是最多的。
- 所有的数据操作被返回都是排序的，排序的顺序是row colmnfamily，qualifier，timestamp
- hbase中没有joins操作，只有get或者scan操作，你需要自己通过行键的设计来完成这个join操作，或者运行相关的MapReduce代码
- version number的是通过HColumnDescriptor定义在每个column family上的，default是3，最好版本号不要太大，这会增加storefile的大小，如果设置成0，表示不需要version功能
### [acid-in-hbase](http://hadoop-hbase.blogspot.com/2012/03/acid-in-hbase.html)
- acid: Atomicity, Consistency, Isolation, and Durability
- hbase使用的MVCC实现acid的，并且没有混合读写的事务
- 在每一个regionserver上，事务号是严格的单调递增的
- 当一组puts或者delete操作开始的时候，首先会拿一个WriteNumber，这个是hbase自增当前最大的事务ID的结果
- 当一个scan或者get操作开始的时候，会拿一个最后提交的事务ID，叫做ReadPoint
- 在hbase中一个写事务由一下几个步骤组成：
	1. 锁住自己需要修改的rows
	2. 拿到writenumber
	3. 先写WAL（Write Ahead Log）
	4. 再写memstore（此时会用writenumber标记所写的keyvalues）
	5. 提交事务，比如：将readpoint指向当前的writenumber
	6. 解锁所有的rows
- 读事务会向这样：
	1. 打开一个scanner
	2. 得到当前的readpoint
	3. 过滤出自己所得到的keyvalues，过滤规则是在memstore timestamp>readpoint
	4. 关闭scanner
- 如果你对上述有疑问的话，说明并发编程功底不错。有一下几点保证上处的正确性：
	- hbase保证所有的事务的提交都是串行的。因为hbase中一个事务一般很短。
	- 只有提交了的事务才对读可见
	- hbase会记录所有未提交的事务，保证提交顺序一定是writenumber小的提交在前面
- <span style="color:red;">[官方](http://hbase.apache.org/0.94/book/architecture.html)hbase保证强一致性，我理解hbase不保证一致性，而是最终一致性</span>，额。。。，所以每个region的MVCC只会在每个regionserver上。这里有必要说一些什么是一致性，对于一个特定的rowkey进行的put操作，要么对所有人可见，要么对none可见。从[hbase代码](https://hbase.apache.org/apidocs/org/apache/hadoop/hbase/client/Consistency.html)上看支持两种一致性：
	1. 强一致性：需要读写的数据只在一台机上
	2. Timeline的一致性，这种一致性将不能看到最近更新的数据
- compactions，就是之前提到的major compactions，会把多个小的store file(会把memstore刷到磁盘上)组合起来，并且把垃圾清理掉

### [HBase and Schema Design](http://hbase.apache.org/0.94/book/number.of.cfs.html)
- 当column family的个数大于两个或三个的时候hbase的性能并不好
- ∆ flushing and compaction在column family很多的时候会导致许多不必要的io开销，因为这两个操作时基于每个region server的，所以最好设计成每次只读一个colmn family
- If ColumnFamilyA has 1 million rows and ColumnFamilyB has 1 billion rows, ColumnFamilyA's data will likely be spread across many, many regions (and RegionServers). 这会导致大量的对 ColumnFamilyA 的scans操作导致很差的性能
-  avoid using a timestamp or a sequence as the row-key.因为这样的数据会落在同一个region server上
- 尽量使行键和列族短小，[这很重要](http://hbase.apache.org/0.94/book/regions.arch.html#keyvalue)
- 把rowkey转成bytes，例如一个string每个字符占一个byte但是转成long型的数则只占8个byte，可以小三倍的size
- 想快速找到最近插入的记录吗？可以使用Reverse Timestamps的方式
```java
Long.MAX_VALUE - timestamp
```
你值得拥有
- <span style="color:red;">pre-split region是很重要的</span>，比方说你的rowkey范围是这样的"0000000000000000" to "ffffffffffffffff"这是二进制的范围，但是你所使用的rowkey是可见字符，这就麻烦了，可能很多regionserver用不到，导致热点问题。下面这个方法比较好

```java
public static byte[][] getHexSplits(String startKey, String endKey, int numRegions) {
  byte[][] splits = new byte[numRegions-1][];
  BigInteger lowestKey = new BigInteger(startKey, 16);
  BigInteger highestKey = new BigInteger(endKey, 16);
  BigInteger range = highestKey.subtract(lowestKey);
  BigInteger regionIncrement = range.divide(BigInteger.valueOf(numRegions));
  lowestKey = lowestKey.add(regionIncrement);
  for(int i=0; i < numRegions-1;i++) {
    BigInteger key = lowestKey.add(regionIncrement.multiply(BigInteger.valueOf(i)));
    byte[] b = String.format("%016x", key).getBytes();
    splits[i] = b;
  }
  return splits;
}
```

- 每个hbase单元的存储最好不要超过10M如果是objects的话可以到50M [object store](https://docs.transwarp.io/4.7/goto?file=HyperbaseManual.html#object-store-chapter)
- [counters](http://cloudfront.blogspot.sg/2012/06/hbase-counters-part-i.html)额，看了下api文档，过时了不再维护了，还是用[LongAdder](http://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/LongAdder.html?is-external=true)吧。他们两都是提供对一个row的column做原子的加操作
- 对于delete的cells使用get或者scan操作还是可以得到的，但是会有[delete markers](http://hbase.apache.org/0.94/book/cf.keep.deleted.html)，亲测有效，delete之后只需要在scan的时候加入这样的参数{RAW => true, VERSIONS => 3}即可
- <span style="color:red;"></span>

### [secondary index](http://hbase.apache.org/0.94/book/secondary.indexes.html)
- 先思考这么一个问题，rowkey是这样user-timestamp，这可以很方便的select by user，但这对于select by time则不容易
- Periodic-Update Secondary Index这种做法的意思是再开一张表，利用map-reduce job去做更新。我感觉可以用[coprocessor](https://www.ibm.com/developerworks/cn/opensource/os-cn-hbase-coprocessor1/index.html)的方法去做。
- Dual-Write Secondary Index ---- write to data table, write to index table
- 其实都差不多，感觉可以看一下phonix是怎么实现的

### [mapreduce](http://hbase.apache.org/0.94/book/mapreduce.html)
- [mapreduce编程模型简要介绍](http://www.flyne.org/article/1121)，map读取input映射成key-value，shuffle把map的结果合并和排序，reduce最后的汇总处理。
- 如果有100个region server就会有100个map-tasks，使用[TableInputFormat](http://blog.csdn.net/yanmingming1989/article/details/7011928)可以方便的完成table2mapper对象的转换，也可以自己定义转换格式，只需要继承TableInputFormatBase。可以自己试一下[从hdfs上读文件做mapper再把结果写到hbase中](http://blog.csdn.net/hadoop_/article/details/11538201)。官方有[input是hbase table的例子](http://hbase.apache.org/0.94/book/mapreduce.example.html)操作性不强，毕竟没有环境。
### [security](http://hbase.apache.org/0.94/book/security.html)
- 首先需要开启Kerberos-enabled HDFS daemons，然后在hbase-site.xml配上Kerberos的操作权限
	- [java连接kerberos](https://www.ibm.com/support/knowledgecenter/en/SSPT3X_3.0.0/com.ibm.swg.im.infosphere.biginsights.admin.doc/doc/kerberos_hbase.html)
	- [源码示例](http://www.voidcn.com/blog/mm_bit/article/p-6104605.html)
	- [kerberos配置](http://www.cnblogs.com/morvenhuang/p/4503478.html#b03)
	- [hbase配置kerberos](http://www.cnblogs.com/morvenhuang/p/4536252.html)
- Access Control没看，人工scan了一下，发现权限的控制还是很细的

### [architecture](http://hbase.apache.org/0.94/book/architecture.html)
- scan -ROOT- .META. 查看region server等信息请使用scan 'hbase:meta'
- [有用的filter](http://hbase.apache.org/0.94/book/client.filter.html)，filter工作在服务器端，这个比较好
- HMaster一般运行在namenode
	- LoadBalancer
	- CatalogJanitor周期性的check and clean hbase:meta表
- HregionServer一般运行在datanode
	- CompactSplitThread找到split然后做镜像压缩
	- MajorCompactionChecker check是不是需要major compaction
	- MemStoreFlusher 周期性的把MemStore to StoreFiles.
	- LogRoller 周期性的check Hlog
- Block Cache 对于table的数据在磁盘上是一个一个的block，block需要load进内存，不能用完就扔吧，所以hbase采用LRU（最近最少使用的清除的算法）干这件事，有意思的是hbase和jvm一样划分出Single access，Mutli access和In-memory access三个优先级来区分block cache的重要程度。jvm大约0.85的heap都是这些cache。下面列出哪些数据会在cache中：
	- Catalog tables: The -ROOT- and .META. tables
	- HFiles indexes：因为HFile是hbase数据持久化的文件格式，为了快速找到数据而不是把整个HFile都load到内存就需要index喽
	- Keys：没错就是rowkey+column family+qualifier+timestamp，所以需要设计的rowkey比较小也是合理的
	- Bloom filters：为了快速检查一个key是否在hbase中存在。bloom filter可以比一般的hash方法少用7/8的空间，因为它用了两个hash函数
- HFile indexes and bloom filters sizes可以在Web UI上查到
- WAL这是个好东西，可以看看[wiki的文章](http://en.wikipedia.org/wiki/Write-ahead_logging)

### [regions](http://hbase.apache.org/0.94/book/regions.arch.html)
- 存储的结构
<img src="store_logic.png" width="800" height="auto"/>

- 
### vocabulary
- Monotonically单调的
- metric_type计量类型
- mutable可变的
- Smackdown打倒
- spit吐出
- sink下沉
- Roll


















































