### 10月30
- pytho性能调优工具time timeit profile
- tuple元组，tuple is immutable
- set的惊人操作

# python高性能编程

## 第一章

- 计算机编程是什么？对数据进行移动和转换得到某种结果，这些操作有时间上的开销

- 素数的定义是什么？如何使用python判断？如何提高判断效率？
- 如何避免GIL带来的单核心问题？使用mutiprocessing或者CPython

- <b>写代码时记得使用单元测试来测试你的代码</b>
- linux的time命令测试一个命令的运行时间 real代表总运行时间，sys系统函数cpu占用时间，user用户函数占用时间，real>sys+user表示程序话费在io上的时间