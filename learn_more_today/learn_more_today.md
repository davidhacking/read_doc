## 2019年9月10日11:24:49

### centos sudo

sudo usermod -aG xxx wheel

sudo vim /etc/sudoers # xxx	ALL=(ALL)	ALL

### python cmd ~[[A

easy_install readline

### /bin/ld: cannot find -lxxx

find /usr/lib -name "\*xxx\*"，有则建立软链接，没有则搜索一发libxxx centos

### graphGL

根据设计感，更加统一的前后端交互

### python base64

base64 每6个bits通过A-Z，a-z，0-9，+/符号表示，即6bits->8bits

```python
import base64
base64.b64encode(b'shiwei')
base64.b64decode(b'fake value')
```

### terminal cmd

ctrl+a，ctrl+e行首，行尾

alt+f，alt+b前进/后退一个单词

### profile

- 一组用于描述用户的数据，档案
- 测量--性能分析--preformance profile

### weakref

弱引用，当A引用了B，B又引用了A，AB都不能被销毁，一般把先创建的对象如A在B中的引用，变成弱引用

### nonzero

\_\_nonzero\_\_，if obj的时候使用，可以使用bool(obj)触发执行

### str与repr的区别

str，repr都是给人看的，repr一般是开发者调试的时候看的

### 编程模型

- main loop event-frame模型
- 协程切换模型

### 如何让学习更快

把新知识关联到老知识上，在已掌握的知识上长出新知识

## 2019年9月11日09:59:58

### 多继承mro的初始化方法

- 打印mro，按照打印的顺序依次初始化

## 2019年9月12日09:06:48

### python re

- search flags， re.search(pattern, string, flags=re.VERBOSE)
- re.escape，通过escape方法可以快速替换pattern中本来就想搜索的元字符

### 代码解构

按流程实现（结构化编程）-> 实现了两个具有共性的代码 -> 找到共性并抽象

解构？解构的过程中其实比较难看到一个完整的流程，总是会被为了处理共性而兼容的代码妨碍

代码其实过程，但是如何理解一个复杂的过程呢？通过看一段过程导致的结果，并理解这一段过程

### 橡皮鸭调试法

- *Once a problem is described in sufficient detail, its solution is obvious.*

## 2019年9月16日10:34:46

### delegate event，分发事件

## 2019年9月18日10:27:19

### 破窗效应

来都来了，破都破了

### git rebase

变基操作，当你做了一些改动，想merge到master上，此时master已经更新了，如果通过merge指令merge就会出现merge的commit，如果用rebase就不会出现

- rebase的原理：先把你的改动都变成patch，先拉取master最新代码，再把你的改动patch上去
- 不过rebase是改变了分支历史的，所以用此指令需要保证你开发的分支是最终版本
- git pull的时候也可以加上--rebase选项，原理是一样的

### python的Queue为什么是线程安全的？

- python的Queue是通过threading.event实现的，就是linux的条件锁
- 不过GIL的存在确实对于线程安全有一定影响，[一些关于list的因为GIL保证的原子操作](https://docs.python.org/3.5/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe)

## 2019年9月19日10:57:50

### 查看python的bytecode

- import dis; dis.dis(module)

### 查看python的source code

- import inspect; inspect.getsource(module)

### 数据证明编程

- Curry-Howard correspondence 柯里-霍华德对应

### python描述符协议

- \_\_get\_\_，访问a.b时，b对象如果实现了\_\_get\_\_，则这个表达式被这样执行b.\_\_get\_\_(a, type(a))

### python lazy_property装饰器

```python
# 自己写吧，通过class实现
```

## 2019年10月12日09:52:22

### 找寻源码，解决问题

- 之前的思路是通过关键字google，然后照查询结果step by step的方式做，可能做完还不明就里，也可能始终解决不了问题
- 解决问题还是要回归问题本质去解决

## 2019年10月16日10:31:47

### go协程的理解

- go的协程可以对应到gevent里的greenlet，go的runtime可以对应到gevent里的hub，
- 理解了gevent就理解了go的协程调度，go协程的调度可以比作python monkey patch后的调度，在网络阻塞或IO阻塞都会调度下一个协程运行
- goroutine的G-P-M协程调度

![img{512x368}](goroutine-scheduler-model.png)

### 计算机科学领域的任何问题都可以通过增加一个间接的中间层来解决

- 什么事计算机科学领域的问题？

### 分类原则

- MECE（Mutually Exclusive Collectively Exhaustive）原则，相互独立，完全穷尽

### 辗转相除法求gcd

- greatest common divisor

  ![img](D:\MF\github\read_doc\learn_more_today\Euclidean_algorithm_252_105_animation_flipped.gif)

```python
def gcd(a, b):
    if a > b:
        a, b = b, a
    if a <= 0:
        return b
    return gcd(a, b - a)
```

## 2019年10月17日17:06:25

### 如何使用python3通过protobuf发送中文？

- 直接把a='时间戳'的变量设置到protobuf定义的message字段中，接收端控制台打印出来的字符串是'\346\227\266\351\227\264\346\210\263'
- 打印出来的字符串实际上是八进制表示的字节码，通过b=b'\346\227\266\351\227\264\346\210\263'，b.decode()就可以还原出原始中文
- 所以也就是说只要保证，发送端设置的中文字段通过protobuf自己的to_str方法打印出来的是这样的字节流就可以了