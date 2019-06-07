# [官网guide](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/index.html)

### tremendous 概念
- cluster default name “elasticsearch”，node will join cluster by cluster name，dev stage prod
- node 在启动的时候就会自动的加入默认名为“elasticsearch”的集群。多个node集群可以是运行在不同机器上也可以运行在同一台机器上
	- 在同一台机器上的node怎么相互发现，使用unicast network discovery
	- 使用9200-9300的port用于http通信，9300-9400用于node间的通信，如果被占用则递增
- index name must be lowercase
- types and document都被存储在index上，doc是被逻辑的存在types里
	- 每个doc被插入的时候可以不显示的提供id，es会自动分配一个
- shards/replica的默认值是5/1，5个shards一份冗余，一共10个shards

### 启动
- ./elasticsearch -Ecluster.name=cluster_name -Enode.name=node_name

### api
- _cat/health?v
- _cat/indices?v
- _bulk?pretty --data-binary "@file"
- _count?q=*
- rename
	_reindex
	{
		"source": {"index": "bank"}, "dest": {"index": "blank"}
	}
- -X DELETE /index_name
- _search 更多过滤规则[executing_filters](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/_executing_filters.html)
	{
		"query": {"match_all": {}},
		"sort": {"balance": {"order": "desc"}}
	}
### java api
- java api 是格式敏感的
- [mapping](http://blog.csdn.net/laigood/article/details/7460489)

### mapping
- 利用mapping可以像mysql一样预定义数据格式，mapping拥有许多不同的数据类型


### 图形化界面
- BigDesk

### vocabulary
- ASAP as soon as possible
- dissect 分析
