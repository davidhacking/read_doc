### AMQP

Advanced Message Queue Protocol

- 信道
  - ID
- 消息路由
  - 交换机，Topic、Fanout、Direct
    - 实际实现只是一张表而已
  - 队列
    - 实际上是通过一个进程实现
  - 绑定
    - 同交换机信息关联存储在一张查询表中

- vhost，用于做权限管理

- 消息持久化
  - 使用comfirm模式，监听nack（通过publish后的delivery_tag和本地维护的确认列表进行）
  - 新建持久化的exchange和queue
- Erlang节点与rabbitmq应用
  - 一个节点下可以运行多个应用，rabbitmq是其中一个，比如：还可以有mnesia（Erlang写的数据库）用于管理交换机和队列元数据
- ACL
  - 通过rabbitmqctl set_permissions 配置权限 读权限 写权限

### 集群

- 集群并不保证消息万无一失，只是保证rmq的高可用，即本来pub和sub连接的是同一个节点，但是那个节点挂了，那么会有集群中的下一个节点顶替上去
- 集群中每个节点都会维护，vhost、exchange、queue和binding的所有信息