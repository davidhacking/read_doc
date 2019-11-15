[阅读effective c++](https://wizardforcel.gitbooks.io/effective-cpp/content/1.html)

- decltype，推到类型，int i=0; decltype(i) a = 0;
- 万能引用（universal reference），T&&表示万能引用，既能接受左值也能接受右值
- 左值引用，右值引用
  - 只能在右边的量是右值，能在左边出现的量是左值
  - 左值：有名字可以取地址，其他的就是右值

- [引用折叠](https://theonegis.github.io/cxx/C-%E4%B8%AD%E7%9A%84%E4%B8%87%E8%83%BD%E5%BC%95%E7%94%A8%E5%92%8C%E5%AE%8C%E7%BE%8E%E8%BD%AC%E5%8F%91/index.html)，引用转发，不经感叹，C++语言层面就要考虑那么多事情
- constexpr，编译期间就能确定的常量表达式

- noexcept，表示函数不会抛出异常，用于编译器优化

- 形参实参，形参：定义时函数的形式参数，实参：调用时传入的实际参数

- 通过模板进行函数调用，在调用时会进行类型推导，实参的引用类型并不能传递到形参

- auto，auto和模板是如此相似，不过也有区别

  - auto可以解析{}为std::initializer_list，T不行

  - 函数返回值定义成auto，其实使用的是模板类型，所以编译器进行类型推导的时候也是用的模板类型推导

- lambda表达式，[捕获](https://zh.cppreference.com/w/cpp/language/lambda#Lambda_.E6.8D.95.E8.8E.B7)，声明：[捕获] <模板> (形参) {操作}

- 友元，通过friend关键字声明，友元函数可以访问类的私有变量和保护变量，但不是类的成员函数

  - 友元一般用于定义一个类外部的函数，但是对类的成员变量访问频次很高的情况

- 返回值类型尾序语法，"->"之后可以声明返回值类型

- decltype(auto)与auto的区别，int i=1; const int& a=i; auto b=a; decltype(auto) c=a; b的类型是int，c的类型是int&

- decltype((x))，比如x是int型，编译器会把decltype((x))解释成int&型
- decltype最终解释成了什么类型可以通过编译器错误信息来查看page35
- hpp，header plus plus，将cpp代码混写在h文件中形成
- 如果想通过运行时打印的方式打印出变量类型，最好使用boost库的boost::typeindex::type_id_with_cvr函数page39
- 使用auto减少不必要的麻烦page44

```c++
for (const std::pair<std::string, int>& p : m) // std::unordered_map的键值是const std::string，所以编译器会每次都复制一个临时对象然后赋值给p，带来不必要的性能问题，直接用auto就好了
```

- 代理类，模拟或增广其他类的类，比如bool值不能有引用，就搞出一个std::vector<bool>::reference的代理类
- “隐形”的代理类似乎和auto无法兼容，因为auto总是会帮我们解析出代理类，而不是我们想要的类

- C++的强类型转换
  - static_cast，不会导致风险，只是说明我想这样转换
  - const_cast，用于const与非const，volatile与非volatile之间的转换
  - reinterpret_cast，对二进制数据的重新解释，例如指针的转换
  - dynamic_cast，存在向上和向下转型
    - 向上转型，子类转成父类
    - 向下转型，比如直接把一个整形转成对象