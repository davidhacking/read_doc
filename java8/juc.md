# 拼多多放羊记三
这波我准备读一读java的java.util.concurrent
管理并发状态的类：CountDownLatch（实现计数器的功能，通常是多个线程一起干活，另一个线程等这些线程干完了再干）、CyclicBarrier（光栅，用法和第一个相反，一般是多个线程一起等待某个状态后同时运行）和Semaphore（多少个线程可以直接进入临界区）
阻塞与非阻塞线程队列：
公平锁非公平锁共享锁：
同步互斥和锁：
有哪些方法可以解决死锁：
### Vector 提供和Array差不多的操作，不过它的扩容是每次加capacityIncrement而不是double
	- 返回fail-fast的iterator，在访问迭代器的过程中vector被修改了会抛出ConcurrentModificationException
	- 返回的Enumeration，不是一个fail-fast的迭代器，是非线程安全的，从下面代码看出这个实现如果在中间插了一个元素elementCount是会变化的这个比较好
	```java
	synchronized (Vector.this) {
        if (count < elementCount) {
            return elementData(count++);
        }
    }
    ```
    - vector同步的实现就是在所有的方法上都加了synchronized关键字，并没有copyonwrite之类的机制

### ReentrantLock 可重入锁，在synchronized的基础上增加了一下其他的特性，同一个线程自己可以多次获取锁，因为在第二次获取的时候会直接返回成功。回想起之前面试的时候又一个人问这个一个线程自己递归调用自己，很有意思然后跪了。这是一个支持公平特性的锁，因为当这个锁可以优先满足等待时间最长的线程。

### CopyOnWriteArrayList 这个类是对于ArrayList实现的一个线程安全版本，采用CopyOnWrite的机制。这个机制貌似有点暴力，因为在做add或set操作的时候需要把Array copy一发。而且返回的iterators不支持修改操作。这个类需要内存一致性的支持，因为某一个类可能先修改了一个元素，另一个线程后面去读取或者去删除这个元素。我已经迫不及待看看add set的实现了。
	- 里面用了一个final取修饰set/getArray方法，表示继承后不能复写。
	- 最重要的array属性是transient volatile的，利用了线程的缓存一致性机制，实现了array对每个线程都是修改了就对所有线程可见，或者对non-thread可见。
	- 看了一发add的实现，并没有很夸张，还是使用了同步的，只是自己先copy了一发，最后又set回去，一个add的复杂度就是O(n)，厉害了

	```java
	public boolean add(E e) {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
            Object[] elements = getArray();
            int len = elements.length;
            Object[] newElements = Arrays.copyOf(elements, len + 1);
            newElements[len] = e;
            setArray(newElements);
            return true;
        } finally {
            lock.unlock();
        }
    }
    ```
    - 这样的实现真的就比使用同步锁更好吗？看了下get操作，很爽，这样就不用同步读了。由此可见COW机制适用于读多写少的应用场景

    ```java
    private E get(Object[] a, int index) {
        return (E) a[index];
    }
    ```

### ConcurrentHashMap 这个类很厉害，说自己支持高并发的修改。这个类并不使用全局的锁锁住所有数据，但是所有的方法是和hashtable一样的（同样不接受nullkey），如果不依赖hashtable实现同步的特性可以直接替换使用。然后就是实现这个类的人真的很喜欢写注释。。。
	-  iterator/enumeration是ConcurrentHashMap某个时候的快照，使用的时候不会抛出ConcurrentModificationException
	- 这个map和适合做频率统计的事情，像这样

	```java
	ConcurrentHashMap<String,LongAdder> freqs
	freqs.computeIfAbsent(k -> new LongAdder()).increment();
	```

	- 这里为了减少key的碰撞把key.hashCode做了这样的优化这样可以减少碰撞，因为对于一个key到底set到哪里是这样的(n - 1) & hash，其中n为table_size

	```java
	(h ^ (h >>> 16)) & HASH_BITS;
	```
	- map其实就是一个keyvalue的array，具体插入的时候ConcurrentHashMap使用CompareAndSwap的方式插入casTabAt，这个是最后插入调用的方法，使用的是sun.misc.Unsafe方法，比较tab(le) i处的值如果是v的话就进行插入c的操作。

	```java
	return U.compareAndSwapObject(tab, ((long)i << ASHIFT) + ABASE, c, v);
	```
	- get的时候是基于缓存一致性协议的方式get的，其实很简单嘛，哈哈

	```java
	return (Node<K,V>)U.getObjectVolatile(tab, ((long)i << ASHIFT) + ABASE);
	```

























