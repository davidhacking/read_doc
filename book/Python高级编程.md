### 使用list comprehension和for-loop-append有什么区别 page24

- 如何编译分析python的bytecode，https://stackoverflow.com/questions/13274110/list-comprehension-optimization，bytecode doc，https://docs.python.org/2.4/lib/bytecodes.html
- 如何阅读python字节码
  - 官网文档：https://www.zcfy.cc/article/an-introduction-to-python-bytecode
  - 通过python实现的解释器调试运行：https://github.com/nedbat/byterun
- http://www.aosabook.org/en/500L/a-python-interpreter-written-in-python.html

```python
import time

size = 10000000  # 917.000 ms 1977.000 ms
times = 10000


def timing(f):
	def wrap(*args):
		time1 = time.time()
		ret = f(*args)
		time2 = time.time()
		print '%s function took %0.3f ms' % (f.func_name, (time2 - time1) * 1000.0)
		return ret

	return wrap


# @timing
def list_comprehensions():
	x = [i for i in range(size) if i % 2 == 0]
	return x


# @timing
def while_construct():
	numbers = range(size)
	s = len(numbers)
	events = []
	i = 0
	while i < s:
		if i % 2 == 0:
			events.append(i)
		i += 1
	return events
```



```asm
list_comprehensions:
 21           0 BUILD_LIST               0         # creates a list.
              3 LOAD_GLOBAL              0 (range)
              6 LOAD_GLOBAL              1 (size)
              9 CALL_FUNCTION            1
             12 GET_ITER            
        >>   13 FOR_ITER                28 (to 44)
             16 STORE_FAST               0 (i)
             19 LOAD_FAST                0 (i)
             22 LOAD_CONST               1 (2)
             25 BINARY_MODULO       
             26 LOAD_CONST               2 (0)
             29 COMPARE_OP               2 (==)
             32 POP_JUMP_IF_FALSE       13
             35 LOAD_FAST                0 (i)
             38 LIST_APPEND              2
             41 JUMP_ABSOLUTE           13
        >>   44 STORE_FAST               1 (x)

 22          47 LOAD_FAST                1 (x)
             50 RETURN_VALUE        
while_construct:
 27           0 LOAD_GLOBAL              0 (range)
              3 LOAD_GLOBAL              1 (size)
              6 CALL_FUNCTION            1
              9 STORE_FAST               0 (numbers)

 28          12 LOAD_GLOBAL              2 (len)
             15 LOAD_FAST                0 (numbers)
             18 CALL_FUNCTION            1
             21 STORE_FAST               1 (s)

 29          24 BUILD_LIST               0
             27 STORE_FAST               2 (events)

 30          30 LOAD_CONST               1 (0)
             33 STORE_FAST               3 (i)

 31          36 SETUP_LOOP              58 (to 97)
        >>   39 LOAD_FAST                3 (i)
             42 LOAD_FAST                1 (s)
             45 COMPARE_OP               0 (<)
             48 POP_JUMP_IF_FALSE       96

 32          51 LOAD_FAST                3 (i)
             54 LOAD_CONST               2 (2)
             57 BINARY_MODULO       
             58 LOAD_CONST               1 (0)
             61 COMPARE_OP               2 (==)
             64 POP_JUMP_IF_FALSE       83

 33          67 LOAD_FAST                2 (events)
             70 LOAD_ATTR                3 (append)
             73 LOAD_FAST                3 (i)
             76 CALL_FUNCTION            1
             79 POP_TOP             
             80 JUMP_FORWARD             0 (to 83)

 34     >>   83 LOAD_FAST                3 (i)
             86 LOAD_CONST               3 (1)
             89 INPLACE_ADD         
             90 STORE_FAST               3 (i)
             93 JUMP_ABSOLUTE           39
        >>   96 POP_BLOCK           

 35     >>   97 LOAD_FAST                2 (events)
            100 RETURN_VALUE             
```

- 从bytecode上看，有以下几个操作不同导致执行速度，list comphrehension（lc）要快很多
  - lc用的是迭代器，而while需要每次减一并和零比较，这个应该差不多吧
  - 在append操作时，while需要每次都load一次数组，获取一次数组的append属性，在进行append，而lc直接append，即直接调用LIST_APPEND原语

### 生成器(generators=coroutines)

- yield
  - 在函数中使用yield var制作一个生成器，调用者使用next获取返回值并使暂停的生成器继续执行
  - 在函数中使用var = (yield)制作一个生成器，调用者需要使用send方法唤醒生成继续执行
  - yield即能返回参数也能接收参数
  - 编写好的生成器同时还有throw（向生成器发出一个异常）和close（关闭生成器）的方法
  - list comprehension将“[”换成“)”就可以实现快速的一个迭代器
  - itertools有多个方法可以生成迭代器
- multitask：https://code.google.com/archive/p/python-multitask/ page 32
  - yield IO阻塞函数？我以为yield怎么了，原来是multitask支持的，通过yield一个YieldCondition对对象，让TaskManager来调度由于IO而阻塞的任务
  - class Queue 和Python的Queue.Queue（文档：https://docs.python.org/2/library/queue.html）实现差不多，即是一个工作队列（Python的Queue.Queue是一个基于python threading的同步队列）
  - YieldCondition，任务管理器（multitask实现的TaskManager）通过任务生成的YieldCondition派生类对象来判断当前任务是否满足timeout条件，调用时使用yield yield_condition_object的形式，因为TaskManager会在condition达到时将任务唤醒，具体可以看基于TaskManager的sleep是怎么实现的
  - FDAction，当一个函数执行时依赖于某个fd ready，这是可以用一个FDAction来处理
  - TaskManager，利用python thread实现的一个非阻塞多任务调度器（cooperatively-multitasking tasks），只能run利用yield编写的任务（即生成器）
- 使用multitask编写的pingpong的程序是如何被任务调度器执行的
  - 对第一个任务进行next运行，并得到next的一次输出（任务可以输出子任务）
  - 对输出的子任务进行处理，即处理子任务上的queue对象，将子任务队列上的一个任务放到TaskManager的queue上在下次循环时执行，下面的代码就是pingpong的核心逻辑

```python
	# 这个是一个TaskManager需要好好理解的成员函数
    def _handle_queue_action(self, task, output):
        # 当对get_waits, put_waits进行操作时实际操作的是self._queue_waits上对应的对象
		get_waits, put_waits = self._queue_waits[output.queue]

		if output.item is output.NO_ITEM:
			# Action is a get
			if output.queue.empty():
				get_waits.append(output)
				if output._expires():
					self._add_timeout(output,
									  (lambda: get_waits.remove(output)))
			else:
				item = output.queue._get()
				self._enqueue(task, input=item)
				if put_waits:
					action = put_waits.popleft()
					output.queue._put(action.item)
					self._enqueue(action.task)
					if action._expires():
						self._remove_timeout(action)
		else:
			# Action is a put
			if output.queue.full():
				put_waits.append(output)
				if output._expires():
					self._add_timeout(output,
									  (lambda: put_waits.remove(output)))
			else:
				output.queue._put(output.item)
				self._enqueue(task)
				if get_waits:
					action = get_waits.popleft()
					item = output.queue._get()
					self._enqueue(action.task, input=item)
					if action._expires():
						self._remove_timeout(action)
```

### 装饰器

- 可以利用装饰器进行参数校验
- 利用装饰器对一个计算量很大的函数进行缓存处理（其实，直接修改原函数就可以了）
- 利用装饰器实现和java中权限控制一样的效果，但是编写要简单许多
- 装饰器也可以实现和with语句一样的上下文效果

### pickle

- 利用pickle可以对任意py对象求一个hashkey，例如：pickle.dumps((obj0, obj1, obj2))

### class

- 多继承，通过类的MRO（Method Resolution Order inspect.getmro(Class)）属性观察多继承方法调用的关系，可能是深度优先搜索实现的，产生诡异的结果，多继承在python中不是一个好的设计方法，可以通过~~另一种设计模式解决~~
- 多继承问题主要是需要判断子类调用方法的时候到底是调用了那个父类的方法，这个问题python2.7以后采用C3算法解决，按照正常思路去做就行了，即不是BFS也不是DFS，https://www.jianshu.com/p/a08c61abe895，merge操作（遍历执行merge操作的序列，如果一个序列的第一个元素，在其他序列中也是第一个元素，或不在其他序列出现，则从所有执行merge操作序列中删除这个元素，合并到当前的mro中。），翻译每个类的mro

```python
class B(A1,A2,A3 ...)
mro(B) = [B] + merge(mro(A1), mro(A2), mro(A3) ..., [A1,A2,A3])
```

- property方法，将一组操作连接到一个方法上，在继承时有奇怪的表现（Page 82）
- \_\_slots\_\_特性，使用\_\_slots\_\_类将不会创建\_\_dict\_\_属性，这样能够节省内存空间，至于没有定义在槽中的属性就无法被动态修改感觉很鸡肋
- \_\_new\_\_方法，该方法在init方法调用之前调用，可以利用这个特性做一些检查工作之类的事情
- type方法可以创建类对象，结合metaclass可以做到对创建类对象的拦截，并修改一些类对象，最后返回修改的类

### cpu、内存和网络使用情况

- cpu
  - 利用装饰器进行profile，page251
- 内存
  - guppy
  - memory_profiler

### 多线程 

- GIL（全局解释器锁），一个进程上的所有对象都被一个全局锁管理,page280

### 设计模式

- 单例模式，Page291，通过\_\_new\_\_实现单例模式
- 观察者，Page300，基于事件的编程方法，需要执行的代码都绑定到事件上
- 访问者，Page303，在walkdir时，可以使用getattr的方式处理每个文件扩展名应该使用哪种函数
- 

### 想法

- 需要知道自己的代码会卡在哪里？例如写一个echo server如果是一个循环搞定的话，这个进程并不能完全利用一个cpu的所有性能，因为sock accept的时候是有io等待的，这个时候进程会处于挂起状态