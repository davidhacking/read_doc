# spring-boot
### features
- servlet container

    委托SpringApplication.run方法启动内置容器，通过复写FailureAnalyzer可以处理容器错误。
    能够通过setWebEnvironment设置是否需要启动web容器(AnnotationConfigApplicationContext | AnnotationConfigServletWebServerApplicationContext)
    - Application events and listeners
        
        通过使用META-INF/spring.factories文件配置自己需要监听的事件
        
        |event|说明|
        |:---|:---|
        |ApplicationStartingEvent|当spring-boot注册了listeners and initializers.|
        |ApplicationEnvironmentPreparedEvent|加载了所有的bean还没开始refresh|
        |ApplicationReadyEvent|refresh调用完毕并且容器已经可以接受request了|
        |ApplicationFailedEvent|初始化失败|
        
- [webFlux](https://docs.spring.io/spring-framework/docs/5.0.0.BUILD-SNAPSHOT/spring-framework-reference/html/web-reactive.html)

    Spring 5 - Spring webflux 是一个新的非堵塞函数式 Reactive Web 框架，可以用来建立异步的，非阻塞，事件驱动的服务，并且扩展性非常好。
    把阻塞（不可避免的）风格的代码迁移到函数式的非阻塞 Reactive 风格代码，需要把商业逻辑作为异步函数来调用。这可以参考 Java 8 的方法或者 lambda 表达式。由于线程是非阻塞的，处理能力能被最大化使用。
    - 举个栗子，http request发送到web server上拉取db上的数据，如果http连接变慢，则函数式编程会使db端传输数据也会变慢
    - 传统的spring mvc的api是基于servlet container的，而webFlux则是基于http-reactive steaming的(tomcat or jetty feature)
- spring-data

|data source|spring-data|
|:----------|:---------:|
|hbase|[spring-data-hadoop](https://my.oschina.net/jackieyeah/blog/745051)|
|elasticsearch|[spring-data-elasticsearch](https://github.com/spring-projects/spring-data-elasticsearch)|
|redis|[spring-data-redis](https://projects.spring.io/spring-data-redis/)|

- 