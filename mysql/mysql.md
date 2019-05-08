# mysql

- [权限控制](https://www.cnblogs.com/Richardzhu/p/3318595.html)

1. 连接权限，登入IP限制
2. 执行权限

- 实现：通过user表控制用户连接server的权限，通过db表控制用户访问db的权限，通过tables_priv表控制访问table的权限，通过columns_priv表控制访问某一列的权限，proc_priv表控制各种存储过程的执行权限
- 存储过程：其实是在mysql中封装了一个调用函数，以供后续调用
- 排序规则，utf8_general_ci 表示case insensitive，排序大小写不敏感，bin表示按二进制排序
- 约束，

- Innodb，mysql中一个插件化存储引擎的一个
  - [B+树](https://www.jianshu.com/p/a5e7a8ed62c1)
    - 数据结构，叶子节点存储数据，主键+所有列数据（聚簇索引）
    - 在数据量很大的时候B+树插入一个数据时需要改变多个已有的节点，效率不高
    - 为什么用B+树实现？将数据按块存储在磁盘上，每次读写取一整块数据是磁盘IO的工作方式，B+树的数据结构刚好满足
    - 通过Insert/Change Buffer 机制，可理解为先将对辅助的修改缓存起来，通过 merge 操作把单个随机修改转换成多个顺序修改提升性能

![img](https://upload-images.jianshu.io/upload_images/17174-8a70f52049697431.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/578/format/webp)

- 连接池
- 管理服务器，包括：备份、安全、集群、配置和权限管理等等
- SQL接口
  - 触发器
- 解释器
- 优化器
- 缓存系统
- 文件存储
  - binlog
  - 索引文件