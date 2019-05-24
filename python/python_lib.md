# python库学习

## ply

完全使用python实现的lex and yacc语法分析

### 什么是lex和yacc

- https://www.kancloud.cn/kancloud/ply/42113

- https://www.ibm.com/developerworks/cn/linux/sdk/lex/index.html
- lex for Lexical Analyzar词法分析器，yacc for Yet Another Compiler Compiler生成编译器的编译器
- yacc，https://www.kancloud.cn/kancloud/ply/42155

### [str与unicode](http://python.jobbole.com/86670/)

- PyObject_VAR_HEAD，表示边长对象，有个ob_size表示size
- ob_shash，string对象的hash值
- ob_sstate，不为零表示是interned的
- ob_sval，一个char数组指针，指向一段ob_size+1大小的内存
- interned机制，一个字符串的缓冲池，可以通过id查看相同的str很多是相同id
- 使用字符串加操作和join操作，前者分配n次内存，后者计算总长度再分配内存
- unicode，是一种将字符对应成数字的映射函数，例如a是97，“我”是6211
- utf-8是编码方式，一个unicode字符需要1-4个字节来存储，utf-8采用变长编码的方式进行处理
  - 如果一个字节以0开头则这个1个字节表示了一个字符
  - 对于n字节的符号（n>1），第一个字节的前n位都设为1，第n+1位设为0，后面字节的前两位一律设为10。剩下的没有提及的二进制位，全部为这个符号的unicode码
- str是一个byte string
- encode unicode->str
- decode str->unicode
- 直接通过s="我"的方式得到的s是一个byte string
- bom格式，就像网页使用charset来表示网页的编码格式，这也是Windows和Linux不同的地方，Windows在存储文件时默认头加上bom格式，而Linux则不进行处理，所以经常在保存文件的时候需要save without bom

### [re](https://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html)

- re.compile Pattern类工厂方法，得到Pattern对象

- re.match直接匹配不需要出现Pattern对象
- [实现正则表达式](https://zhuanlan.zhihu.com/p/21706179)

### multiprocessing

- Process，提供和threading类似的接口，process.start()调用forking.Popen，之后会像linux一样创建子进程，子进程空间中会调用Process对象的bootstrap函数
- forking.Popen

- [Pool](https://blog.csdn.net/liuxingen/article/details/72605343)，会开启handle_tasks、handle_results和handle_worker，前两个好理解一个是把任务从task_queue放到inqueue，和把outqueue中的结果对应到ApplyResults上，handle_worker的存在是和线程池的实现不一样的，每个worker是一个process，所以在运行完任务后process会退出，然后由handle_worker线程创建出新的worker来维持pool的worker数量
- apply_async返回result，异步提交任务，最后执行完成后通过result.get获得

### os

- fork，子进程返回pid为0

### django

- 架构，本身是一个单个多线程的框架，依照WSGI协议实现了WebServer和WebApp，开发者只需要专注于WebApp端的业务逻辑开发即可
- Web Server，一个由Socket编写的HTTP服务器，接收用户请求并封装成http request对象，交给Web App处理，即把environ和start_response交给Web App
- Web App，django中的MVC，M由models.py构成，V由templates下的html构成，C由views.py和urls.py构成，Web App调用start_response向Web Server返回执行结果
- 路由配置，django框架会读取settings.py中的ROOT_URLCONF属性，django收到请求后会通过urlresolver使用正则匹配到相关的函数处理

- [models.Field中是如何定义出具有类型的变量的](https://www.cnblogs.com/StitchSun/p/7723983.html)，通过python的get、set和metaclass实现的，定义NameProperty和Validated分别处理get、set和validate功能，通过metaclass让设置的属性具有名字
- python manage.py sqlmigrate YOUR_APP_LEABEL查看django将会执行哪些sql语句
- django实现了Web Application开发框架
- 并发：采用gunicorn+nginx+gevent

### [uWSGI](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/)



### Tornado

### Flask

- [flask中同样用threading.local解决request问题](https://www.zlovezl.cn/articles/charming-python-start-from-flask-request/)
  - 利用werkzeug库提供的LocalStack方法，实现在不同的线程和协程中的对象值是不同的
  - LocalStack通过检测当前线程或协程的id，并使用一个dict实现查找方法

### Gunicorn

- Web Server Gateway Interface，在Web Server与Web App之间的一种通信协议，WSGI还定义了middleware中间件，当WebServer会把request一次交给每个中间件处理后得到最终WebApp返回的response给WebServer渲染
- 

### metaclass

- 在类定义之前对整个类对象操作一遍

### type

- 可以用来动态定义一个类例如：type('class name', (object, ), {'property': 'value', 'func': lambda x: x})

### partial

将以后函数包装一遍，达到固化了已有函数的参数，然后返回一个新的函数的目的

### Annotation

- 装饰器，可以用于实现log和timeit等功能，相当于面向切面编程

## python3

### protobuf

- install
  - 选择版本，https://github.com/protocolbuffers/protobuf/releases
  - 安装protoc，例如：[windows](https://github.com/protocolbuffers/protobuf/releases/download/v3.7.0/protoc-3.7.0-win64.zip)
  - python3 setup.py build, python3 setup.py install
- 编码
  - 1byte，1-15，2bytes，16-2047，把小的标签值分配给常用的消息，大的给不常用的这样可以减小消息大小
- 字段类型
  - repeated，list
  - reserved，预留标签
- 消息类型
  - oneof，限定只有一个字段生效
  - Any，嵌套式类型

- rpc
  - 