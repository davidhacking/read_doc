# [Elasticsearch 权威指南](https://es.xiaoleilu.com/010_Intro/05_What_is_it.html)
### features
- 分布式高可用的搜索集群
- 
### install
- [download](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.tar.gz)
- [xpack](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/setup-xpack.html) es安全，监控，告警，通知，图表，机器学习
- run：
    ```bash
      ./bin/elasticsearch > logs/`date +%Y-%m-%d.%H:%M:%S`.log 2>&1 &
    ```
- stop:
    ```bash
      curl -XPOST 'http://localhost:9200/_shutdown'
    ```
- 配置：elasticsearch.yml
- 想要更好的使用命令行的方式启动es可以搜索github elasticsearch-servicewrapper


### java client(use port: 9300)
- node client 节点客户端，作为无数据节点加入集群，知道集群中数据的位置
- transport client 传输客户端，发送请求到节点

### document
- es集群上会有多个索引(indeices)（数据库），每个索引有多个类型(types)（表），每个类型有多个文档(document)（row），每个文档上有多个字段(fields)（column）
  1. 每个索引可以被配置成多个shard，每个shard可以有多个replica，这造就了高可用，每个shard其实是一个lucene index
  2. Multi Tenant with Multi Types. 多需求可以对应多个类型，可以理解为多个需求多个表
  3. 对每个文档的操作保证acid
  4. 越多的shards越能带来更好的index性能？越多的replica越能保证系统的稳定性。
- 倒排索引，一般统计的时候是整个语料库中哪些文档出现了哪些词，但是如果需要根据词来找出文档并且排序就需要倒排。


### curl
- download file
以remote name作为file name存储
```bash
curl -L -O {{url}}
```
- 发出application/json请求
```bash
curl -X<VERB> '<PROTOCOL>://<HOST>:<PORT>/<PATH>?<QUERY_STRING>' -d '<BODY>'
curl -XPOST url -H --data-binary "@data.json"
```

### 有些坑文档里没有，然后自己一脚就踩上去了
- es5.5.1启动至少需要1G内存，在运行了hbase的虚拟机上运行es就呵呵了

### 有用的api
- list all indices
```bash
curl 'localhost:9200/_cat/indices?v'
```

### keyword
- terms = tokens = 一个单位分词






























