# effective python

python的effective完全不如java的effective啊，reduce visual noise。。。

### diff between bytes, str and unicode

- unicode -> bin data encode
- bin data -> unicode decode

### 写helper函数

- 不要利用python的语言特性而把代码只写成一行，写成易读的代码

### 谨慎使用start\end和stride的方式来slice数组

- 这不易读
- 在slice的过程中如果stride存在那么有可能会进行新的内存分配和copy

### list comprehension就能做到map和filter需要做的事情，且非常易读

### 对于大型的list comprehension使用迭代器生成

- 即使用()而不是[]

### 使用enumerate而不是使用range来获得一个list item的index，因为enumerate使用迭代器实现

### zip在py2里并不是使用生成器实现可以使用izip

### 使用try/except/else使程序易读Page41

### just raise exception if args is wrong Page42

### 使用py中的闭包时可能会遇到奇怪的问题

- 当你在闭包中赋值一个闭包外的变量的时候，会被判定成一次定义变量的操作，因为python的作用域是从当前函数的作用域开始判断的，顺序FEGB，F当前函数，E闭包，G全局变量，B内置函数
- 在py3中可以用nonloacl的方式生命

```python
b = 3
def f(a):
    print(b)
    b = 3
    print(b)
```

- 这段代码会报错，因为解释器在解释f函数时，发现b在f中定义的，所以呵呵，第一个print(b)是有问题的，b并未定义

### 传递的参数是一个迭代器

- 如果传递的参数是一个迭代器，那么可能多次使用这个迭代器会导致在第一次调用后迭代器被耗尽

### 使用*args传参的问题

- py虚拟机会把args解释成生成器，并重新构建一个tuple

### 如果函数传递的参数是可变的，则通过None作为默认参数

- def log(msg, time=datetime.now())，time只会在第一次调用的使用初始化，以后都不会调用datetime.now()了

### class的继承、多态和封装在持续开发中的应用Page64

- python的dict、list和tuple可以使你完全不用去定义数据类型也可以方便的开发，但是这会给维护的人产生巨大的麻烦
- 在第一次迭代需求的时候需求是A，到第二次迭代的时候需求变成了B，需求在一定程度上是有继承的，所以也可以在开发的时候通过继承的方式去维护。但这似乎非常难做到，因为一开始设计的时候就不知道后面可能的变化，只能确保一开始设计的时候每个模块尽可能小，容易改变

### 通过classmethod方法实现构造函数的多态

- python的init函数并不支持多态，通过classmethod可以很好的弥补这一缺点
- 可以参考24条，把不通用的过程代码放到customer class里实现

### 继承并实现collections.abc来实现某些类

- 比如需要实现一个类对象可以通过下标访问，通常会实现getitem方法，也可以通过继承Sequence类实现

### 通过@property装饰器实现访问属性时的特殊行为

- python对属性进行访问和设置时不需要实现get和set函数
- 通过@property方式实现可以达到简化代码的目的

### 通过描述符协议实现类的属性定义与管理分离

- 这种分离有什么好处？可以统一的写一些逻辑代码在某些属性上
- 协议解析如下：

```python
class TestGet(object):
    def __init__(self):
        self.val = 'test'

    def __get__(self, instance, typ=None):
        print("A.__dict__['b'].__get__(a, A)")
        return self.val

    def __set__(self, instance, value):
        print("A.__dict__['b'].__set__(a, value)")
        self.val = value
class A(object):
    b = TestGet()
if __name__ == '__main__':
    a = A()
    print(a.b)
    a.b = 'tes'
    print(a.b)
```

### 通过WeakKeyDictionary保证描述符类不泄露

### \_\_getattr\_\_和\_\_getattribute\_\_的区别

- 前者只会在访问的属性不出现在dict里是访问
- 后者每次都会先被访问，为了避免无限递归访问，可以通过super的getattribute访问访问

### 元类的使用

- 在通过\_\_init\_\_实例化对象时，首先会调用元类的\_\_new\_\_函数，同时传递meta，name，bases，class_dict四个参数
- 即元类是在产生类之前先运行的类，调用顺序：初始化类，调用元类new函数，调用init函数初始化对象

- 借助元类来做python对象Entity与数据库表进行映射

### 使用subprocess替换越写越庞大的shell脚本

- 编写两个进程通过管道通信协作完成任务的方法：先编写两个进程的代码逻辑，在把两个进程跑起来

### 利用Queue使Thread协同工作

- Worker线程何时退出？
- 多线程协作时如果线程工作一个快一个慢，导致内存膨胀怎么办？
- 初始化Queue时设置size，通过get_wait和put_wait进行get，put数据
- 通过task_done通知线程完成，queue的join方法等待的是整个queue中的每个item都task_done，应该是有一个内部的计数器

### 利用yield from进行生成器调用

- yield from的好处是简化从一个生成器调用另一个生成器的语法
- yield from的本质就是在yield from处展开上一个生成器的调用
- yield和yield from对比，yield from可以接受return值到变量，而yield只是简单的读取所有生成器的值

### 协程程序设计

- 关注点的分离
- 协程的程序设计还是遵循goroutine的比较好吧，虽然goroutine的协程程序设计已经是基于go的runtime调度做的了，不过通过消息通信的协同机制还是比较好理解
- python的协程程序设计也应该基于gevent去设计，自己通过yield设计一个协程程序的话，还得自己造协程管理器的轮子

### python并行计算

- 通过concurrent.futures的ThreadPoolExecutor和ProcessPoolExecutor实现并发计算
- ThreadPoolExecutor，是单进程多线程实现的，为啥会比直接计算更快？
- ProcessPoolExecutor，是多进程实现的，没有GIL锁的限制，所以比较快，但是进程间的通信其实是比较费时间的

### 利用contextmanager写with语句

### 利用pickle对python对象进行序列化

- pickle感觉一般用不到，现在的程序都是追求快速的，写磁盘，序列化反序列化只会减慢执行速度
- pickle可以用于存档

### 用\_\_all\_\_来规避import*带来的问题

