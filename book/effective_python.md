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

### 使用*args传参的问题

- py虚拟机会把args解释成生成器，并重新构建一个tuple

### class的继承、多态和封装在持续开发中的应用Page64

- python的dict、list和tuple可以使你完全不用去定义数据类型也可以方便的开发，但是这会给维护的人产生巨大的麻烦
- 在第一次迭代需求的时候需求是A，到第二次迭代的时候需求变成了B，需求在一定程度上是有继承的，所以也可以在开发的时候通过继承的方式去维护。但这似乎非常难做到，因为一开始设计的时候就不知道后面可能的变化，只能确保一开始设计的时候每个模块尽可能小，容易改变