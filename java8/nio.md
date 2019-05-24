# JavaNIO

### IO模式

- BIO，blocking io，我要读
- NIO，non-blocking io，可以读了通知我（Reactor模型）
- AIO，async io，读完了告诉我（Proactor模型）、

### NIO处理过程

- 一个Reactor线程用于select connect、read和write事件
- handle_read处理相关业务逻辑，处理的业务逻辑根据需要提交给相关的线程池处理

### [NIO场景](https://tech.meituan.com/2016/11/04/nio.html)

- 爬虫，底层http连接采用socket实现，通过map维护socket池
- RPC框架，NIO+长连接

### 多线程的本质

- 利用多核
- IO阻塞时可以转让CPU处理其他任务