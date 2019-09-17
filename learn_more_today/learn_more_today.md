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



