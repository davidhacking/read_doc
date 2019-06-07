# [了解nginx原理](http://tengine.taobao.org/book/chapter_02.html)
### 设计的核心思想
- 别增加无谓的上下文切换
- 异步非阻塞的方式处理
- 具体的系统调用：select/poll/epoll/kqueue，有必要明白这些开发模型
### 运行模式
- master worker
- 每个worker通过先获取accept_mutex锁的方式获取listenfd的控制权限（socket），一个请求只会被一个worker处理
- 如何控制每个worker能够平衡的处理每个连接：ngx_accept_disabled用于表示当前worker的负载情况，负载过大则不获取锁
### http请求，文件协议，所以是一行一行的读取处理的
- 请求行，method uri http_version
- 请求头，
- 请求体
- 响应行
- 响应头
- 响应体
### 处理函数
- ngx_http_process_request_line处理请求行
- ngx_http_read_request_header读取请求数据
- ngx_http_parse_request_line解析请求行

- ngx_http_process_request_headers处理完请求行后使用这个函数继续处理
- ngx_http_read_request_header读取请求头
- ngx_http_parse_header_line解析一行请求头

- ngx_http_process_request处理请求体
### 性能调优
- 关掉keepalive最后会产生比较多的time-wait状态的socket
### [配置](http://www.nginx.cn/doc/)
- event
	- worker_connections: max_clients = worker_processes * worker_connections/4
- http
	- include包含一个文件进来
	- application/octet-stream一般的字节流
	- sendfile，普通的sendfile一般需要经过磁盘读取数据到kernel buf，再到user buf，在到kernel buf的socket，在到协议栈，linux2.0采用了更佳好的方案不需要经过用户态
	- server_name，用于对client request中的host做处理
	- [location匹配方式](https://moonbingbing.gitbooks.io/openresty-best-practices/ngx/nginx_local_pcre.html)，遵循最大匹配规则