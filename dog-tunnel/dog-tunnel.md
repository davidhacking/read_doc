# dog-tunnel

## 简介

- github https://github.com/vzex/dog-tunnel
- 狗洞是个使用go编写的解决tcp的p2p通信问题的程序

## 运行

例如：运行一个ssh的服务

<http://dog-tunnel.tk/case>

ssh server端，应该叫做被ssh的客户端

./dtunnel -reg xxxdddd -local 127.0.0.1:22 -clientkey kkkkk

ssh client端，ssh控制的客户端

./dtunnel -link xxxdddd -local :4225 -clientkey kkkkk #把远程客户端的ssh端口映射到本地的4225端口

ssh -p 4225 root@localhosts

you can get the dtunnel from scp -P 6722 david@dclab:~/dtunnel