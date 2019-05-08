# [hbase api dco](https://archive.cloudera.com/cdh5/cdh/5/hbase-0.98.6-cdh5.3.3/devapidocs/index.html)
准备使用TDD开发一个hbase数据导入工具，准备使用和之前不一样的方式开发，就是自己阅读官方api文档，然后写代码。
而不是google一发这个代码可以用然后贴上去
看个文档居然要翻墙
### client.locking
    - 这个包里只有这一个类EntityLock
    - 这个锁很厉害，可以锁住 Table, a Namespace, or Regions，在HMaster上
    - 当你开启一个锁之后在client上会建立一个周期性发送heartbeats到HMaster维护这个锁
    - 如果发送heartbeats超时则这个锁就被释放了
    - 使用lockServiceClient初始化
### client 
    - Append 这个类只对单一一行做追加操作
    - HTablePool 是一个不推荐使用的类 需要使用getTable得到一个table使用。
        再使用putTable或者HTableInterface.close()把用完的table放回去
    - HConnectionManager 根据configuration管理connection，如果之前连接过则使用相同的connection。
        下面三个类在传入config后创建的HConnection都是通过这个类
    - HTable 不是一个线程安全的类，当多线程操作一个HTable的时候会失败
        HTable是HBase的client，负责从meta表中找到目标数据所在的RegionServers。
        当定位到目标RegionServers后，client直接和RegionServers交互，而不比再经过master。
    - HConnection 维护一个hbase所有server的通信列表，如哪台机是master，哪些是regionServer。当这些机器失效后会同步相关信息
    - HBaseAdmin 管理所有表的metadata，提供所有的管理员的功能，如： create, drop, list, enable and disable tables