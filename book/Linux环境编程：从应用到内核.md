### 0.4.2 C库函数

- 什么是系统调用？实际上就是调用C的库函数，大多数系统调用都被封装在了libc中

### 0.4.3 线程安全

- 什么是线程安全？线程安全就是符合正确的逻辑执行过程

- 解决线程安全的核心在于：对共享变量实现串行化访问

### 0.4.6 阻塞调用与非阻塞调用

- 阻塞调用，除非调用出错，否则进程将一直变成内核态直到调用完成

