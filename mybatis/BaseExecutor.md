# 来自mybatis的坑
### localCache机制
- 对于同一session的缓存机制
- 这东西坑的地方在于对于同一sqlSession，如果不进行session close的话就不会触发localCache clear
    也就是说所有的查询都会在java heap中，然后就会oom，真可怕。
    1. 一种就是直接对session进行close，别担心，和数据库的connection并不会关闭而是返还到connection pool里
    2. 第一是设置flushCacheRequired这个字段，每次查询的时候就会清除所有cache
    3. localCacheScope=STATEMENT，这样localCache只会在statement执行的时候使用，
           在同一个sqlSession中，对于不同的调用者将会返回不同的数据
### cache机制
- cache是跨session，可以看看以下关键词包含的文档，程序员没事看看文档陶冶情操
- [cacheEnabled](http://www.mybatis.org/mybatis-3/configuration.html#settings)
- [cache](http://www.mybatis.org/mybatis-3/sqlmap-xml.html)
- [cache-ref](http://www.mybatis.org/mybatis-3/sqlmap-xml.html)
- [useCache](http://www.mybatis.org/mybatis-3/sqlmap-xml.html)
- [flushCache](http://www.mybatis.org/mybatis-3/sqlmap-xml.html)