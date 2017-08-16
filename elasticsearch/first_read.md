# [Elasticsearch 权威指南] (https://es.xiaoleilu.com/010_Intro/05_What_is_it.html)
### install
- [download](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.tar.gz)
- [Marvel]es的监控管理工具
    - 安装与禁用
    ```bash
      ./bin/plugin -i elasticsearch/marvel/latest
      echo 'marvel.agent.enabled: false' >> ./config/elasticsearch.yml
    ```
    - [web控制台](http://localhost:9200/_plugin/marvel/)
- run：
    ```bash
      ./bin/elasticsearch > logs/`date +%Y-%m-%d.%H:%M:%S`.log 2>&1 &
    ```
- stop:
    ```bash
      curl -XPOST 'http://localhost:9200/_shutdown'
    ```
- 配置：elasticsearch.yml

### java client(use port: 9300)
- node client 节点客户端，作为无数据节点加入集群，知道集群中数据的位置
- transport client 传输客户端，发送请求到节点


### curl
- download file
以remote name作为file name存储
```bash
curl -L -O {{url}}
```
- 发出application/json请求
```bash
curl -X<VERB> '<PROTOCOL>://<HOST>:<PORT>/<PATH>?<QUERY_STRING>' -d '<BODY>'
```

### 有些坑文档里没有，然后自己一脚就踩上去了
- es5.5.1启动至少需要1G内存，在运行了hbase的虚拟机上运行es就呵呵了