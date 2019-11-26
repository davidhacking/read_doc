### 通过builder模式构建对象

- 让代码可读性更强
- 与javabean构建对象相比，具有线程安全性？

### 单例的实现

- 类锁+volatile+双重校验
  - volatile保证一个线程写，另一个线程必能读取到，因为在系统层面上保证了不仅仅写cpu缓存，还会写内存
  - 无法防止通过反射修改，但是程序自己破坏自己，为毛要考虑这种奇怪的问题呢？
- [枚举实现](https://www.jianshu.com/p/4e8ca4e2af6c)
  - 每个枚举对象都是static的，static在类加载的时候会初始化
  - 类的初始化通过loadClass方法实现，这个方法保证了线程安全
  - 实际是把线程安全实现交给了jvm

### 减少对象的创建

- 把方法中不变的量通过final变量+static代码块的方式初始化
- page19展示的包装类的问题太经典了

### 内存泄漏问题

- page21的内存泄漏问题太经典了
  - 不过这个例子里不是应该是不可达的数组被释放，然后数组上的元素也被释放吗？
- 对于这种能自己回收垃圾的语言，还是得清楚代码运行过程中，内存是怎么被安排的，自己心里走一遍后就会发现问题（没错，这段代码的问题，我看出来了）
- 如果类中的内存是自己管理的，就应该警惕是否存在内存泄漏的问题了，即一个对象成为垃圾后什么时候会被回收

### equals方法

- 自反性，自己等于自己，通过==保证，比较引用
- 对称性，A==B则B==A，通过instanceof方法保证，再通过强制类型转换
- 一致性，如果对象变，相等的对象应该始终相等
- 同时复写hashCode方法，equals如果相等，hashCode也必须相等，反过来不成立，因为有hash冲突

### 覆盖toString()方法

- 

### volatile关键字什么时候用？

- 对于lazy init的变量（因为需要cache）

## 工具

- Heap Profiler

### sed命令

读取

- 模式空间（活动缓冲区、pattern space）、保留空间（暂存缓冲区、hold space）

  - 应用

  ```bash
  sed -e '/test/h' -e '/check/x' example #互换模式空间和保持缓冲区的内容。也就是把包含test与check的行互换。
  ```

- 选项
  - -n silent模式，对于不在命令中处理的行都打印
  - hold space -> pattern space
    - g复制
    - G追加
  - pattern space -> hold space
    - h复制
    - H追加
  
- 命令，[address range]\[sed command] 或者 [regex pattern]\[sed command]
  - sed command
    - s替换
    - p打印
    - g全局
    - lb goto label
    - N循环代码块
    - ! 逻辑运算符非的意思，反选
    - $ 文件末尾
    - {} 语句块

## 思考

### 每个出现重复调用的地方都需要考虑性能问题

- 需要考虑的循环
  - for循环内
  - 反复调用的函数内
- 需要考虑的问题
  - 类的初始化
  - for循环的数据量
  - 网络读取的数据量