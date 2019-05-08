# 放羊记二
前面读了一发hbase的apache官方文档，感觉自己吹逼的本事厉害了一些。
在读到最后官方文档说hbase是在hdfs上的，所以很有必要再读一发hdfs。希望能够读完。
### [Apache Hadoop 3.0.0-alpha4](https://hadoop.apache.org/docs/current/) 2017-06-30更新的。读这个文档准备做两件事：
	- 读hdfs的文档
	- 理解hadoop streaming
### [hdfs](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
	- hdfs 提供对错误的发现和自动快速恢复
	- 支持流式读取数据集，但hdfs适用于高吞吐量的场景而不是低延时的用户交互场景
	- hdfs适用于write-once-read-many的文件操作场景，当一个文件被创建后，最好后续的操作都是 appends（追加） or truncates（截断）的，比如：爬虫应用或者MR应用
	- 计算需要发生在数据所在的机器上这样hdfs的性能会比较好，而不是计算过程中需要moving data
	- 
### vocabulary
	- quotas 定额