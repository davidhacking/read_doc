# libevent

http://www.wangafu.net/~nickm/libevent-book/

https://github.com/KelvinYin/libevent-src-analysis/blob/master/libevent%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90.md

https://blog.csdn.net/zhouyongku/article/details/53434623

http://gocode.cc/project/11/article/38

### reactor模式与proactor模式

- 事件分离器：等待事件，调用相关处理函数

- reactor：注册事件，事件分离器等待事件，事件分离器同时注册事件的人处理事件
- proactor：把事件的处理函数交给事件分离器，事件分离器等待事件和时间处理完成，然后通知调用者

### select

- waits until a socket from one of the reading, writing or exceptions sets is ready，then return the ready socket for you to use
- 线性扫描所有文件描述符，选出能够读、写或error的，有最大文件描述符数目限制
- 跨平台
- 利用fcntl把一个socket置为一个异步的socket，利用这个api你可以利用errorno==EAGAIN判断当前socket是否可用，写一个spin-polling（轮询）去实现一个socket-server

### poll

- 和select一样，去掉了文件最大描述符限制

### epoll

- Linux内核直接支持
- 采用内存映射技术省去了文件描述符复制的问题
- 实现方式：内核对需要监视的文件描述符进行扫描，则采用回调机制激活这个文件描述符

### tcpdump

- dump the traffic on a network
- -i 指定网卡 lo eth0，通过ifconfig查看
- host指定一个host进行监听 sudo /usr/sbin/tcpdump -i lo tcp port 4444 and host 127.0.0.1
- src > dst: flags data-seqno ack window urgent options
  -  flags 标志由S(SYN), F(FIN), P(PUSH), R(RST),
- 如何把一个应用程序收发的包和tcpdump抓的包关联起来

### 编写一个libevent

- 利用event_config初始化event_base
- 使用event_assign添加一个event
- 调用event_base_dispatch轮询，事件触发后将会调用event_assign赋值的函数回调

### 对socket的监听

- https://blog.csdn.net/luotuo44/article/details/39344743

- 可读：可读比较简单，只要监听fd的缓冲区是否有数据
- 可写：监听fd的缓冲区是否满了，如果没满就能写，但要在有写需求的时候才监听，不然每时每刻都是可写的

### 工作原理

- bufferevent结构体定义了input和output两个evbuffer类型的变量，用于分别处理读写事件，可以通过bufferevent_socket_new实现

### bufferevent_socket_new

- 在bufferevent_init_common中调用evbuffer_new()初始化input和output
- 在event_assign中初始化bufferevent中的ev_read和ev_write事件
- 在evbuffer_add_cb中给output添加了一个callback bufferevent_socket_outbuf_cb
- 

### bufferevent_write

- 调用bufferevent_write时，libevent会把需要写入socket缓冲区的数据全部复制一遍，你可以放心释放
- 直接调用evbuffer_add把数据复制到evbuffer里，调用buffer.c:1747 evbuffer_add函数
- evbuffer_add又会调用buffer.c:517 evbuffer_invoke_callbacks_函数，回调写缓冲区事件，即调用buffer.c:459 evbuffer_run_callbacks函数，这个是注册到evbuffer的一个事件回调，当有数据写入的时候会被调用
- 而这个callback实际调用的是哪个回调函数？实际调用的是在初始化bufferevent对象的时候（bufferevent_socket_new）注册的这个evbuffer_add_cb(bufev->output, bufferevent_socket_outbuf_cb, bufev);
- bufferevent_socket_outbuf_cb定义在bufferevent_sock.c:129，继续调用bufferevent_add_event_，bufferevent_add_event\_调用event_add，这个函数实际是自己注册一个写事件到libevent中，等可以写的时候写

### evbuffer_add

### event_add

### 想法

- c/c++语言可读性较差，想查一个文件中一个函数是哪个库的，一个库在这个文件中被调用了几次都很麻烦
- 还是库的问题，c/c++的库都无法通过方便的方式共享，这导致了开发者重复造了很多轮子，换一个项目可能就造一个轮子
- c/c++各种库在网上的支持帮助信息很少，而且很多信息有时让人摸不着头脑
- c/c++使用库的include方式是最令人头疼的，编译器不能像java一样帮我们处理好声明和实现的话，其实只需要写一个实现文件就行了
- c/c++库的学习成本贼高，例如：libevent为什么new一个libevent需要传递那么多参数？libevent库的调用中各种上下文关系也需要理清楚。。。
- c/c++的报错也不人性化，让小白一看报错信息一开始处于懵逼状态，例如：我明明是第n行忘记写分号，但报错信息却是n+1行的