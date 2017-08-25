# [mybatis-spring](http://www.mybatis.org/spring/)
### why
- 到底应该踩到坑了去学习，还是一开始学完整再去编码？
- 一开始学习官网晦涩难懂，然后学习别人的博客感觉照葫芦画瓢挺简单，后面出了问题还是得好好学习官网，
    所以一开始学习的时间可以放长一些，但是出了问题还是得好好学习一下官网的。
- 学习博客就有点像盲人摸象，学习官网可以整体的学习整只大象，明白里面的所有机制
### mybatis-spring
- 为在spring中更好的暴露sqlSession接口的组件
### org.mybatis.spring.SqlSessionFactoryBean
- 输入 dataSource, mapperLocations(指定mapper文件位置) 输出 sqlSessionFactory
- sqlSessionFactory 用于 open sqlSession
-  如果只是单独使用mybatis则可以使用SqlSessionFactoryBuilder来创建 sqlSessionFactory
- configLocation可以用于指定mapper的映射文件的位置
- 为什么要sqlSessionFactory，因为专门有一个类用来管理数据库会话，并提供统一接口，能够方便地切换数据源

### MapperFactoryBean
- 输入 mapperInterface(即 Mapper接口), sqlSessionFactory 输出 具体的 mapper
### MapperScannerConfigurer
- 自动创建MapperFactoryBean生成SqlSessionFactoryBean
- 主要用作mapper映射文件的扫描器
### transactionManager
- 输入 dataSource
- mybatis利用spring提供的DataSourceTransactionManager对事务进行管理
- 基于容器的事务管理器CMT(Container managed transactions), 即在sqlSessionFactory中配置一个mybatis的ManagedTransactionFactory
- 在使用了transaction manager的代码中不能显示的调用sqlSession.commit，不然会抛出UnsupportedOperationException
### SqlSessionTemplate
- 可以通过SqlSessionFactory来创建，这是mybatis-spring的核心
- 这是个线程安全的接口
### Spring Batch 虽然提供了分页功能，但是没见哪个项目用过基本都自己实现
- MyBatisPagingItemReader
- MyBatisCursorItemReader
- MyBatisBatchItemWriter