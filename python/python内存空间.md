# python内存空间

## python对象实现

- 对象索引结构

![1538986623838](D:\MF\doc\python\py对象内存索引.png)

- 整数缓存池，和java一样python也有自己的整数缓存池用于加速，整数缓存池在一开始就会分配，并且使用数组存储，这样在内存中可能会有一些连续的整数段

  ![1538989905233](D:\MF\doc\python\整数缓存池内存分配.png)

## 在内存中判断对象的类型，并读取对象的值

- 找到某个类型为int的对象（如：整数缓存池）
- 通过ob_type找到PyType_Int的地址，判断需要读取的内存对象的类型地址是否指向这个地址
- 根据PyIntObject结构定义读取int值

## python运行时

### python解释器

![1538991129675](D:\MF\doc\python\py解释器关系.png)

- PyInterpreterState python解释器进程

  ![1538990852435](D:\MF\doc\python\python_interpreter.png)

- PyThreadState python线程

- frame 执行栈帧，包含了执行代码段信息以及本地、全局变量信息

- 可以使用系统api查找现有的threadid找到相关threadid对应的PyThreadState对象，再根据指针关系进行下一步查找到frame对象和PyInterperterState对象

















