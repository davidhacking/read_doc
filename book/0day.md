## 关于内存的基础知识（from 0 day）

- 0 day表示被发现的漏洞，但软件生产商未发现，会未放patch进行修复

- PE(Portable Executable)，\*.ext，\*.dll

- 一个可执行文件的代码段：

  - .text，编译后的机器码，可执行二进制编码，可用于反编译和调试
  - .data，数据段，如：静态变量，全局变量等等
  - .idata，动态链接信息，如：动态链接库和文件信息等
  - .rsrc，程序的资源，如：图标、菜单等等
  - .reloc、.edata、.tls、.rdata

  ```python
  # NeoX的client.exe的段为
  .text
  .rdata
  .data
  .idata
  .gfids
  .tls
  .00cfg
  .rsrc
  .reloc
  ```

- 装载基地址Image Base，EXE的装载基址是0x00400000，DLL的装载基址是0x10000000

  - VA，虚拟内存地址
  - RVA，VA=RVA+ImageBase
  - deadbeef与“烫”，编译器填充已分配但未初始化的内存使用的字符串也是不一样的，例如VC用0xCC，0xCCCC在Unicode里是“烫”，linux用deadbeef填充

  ```python
  import pefile
  pe = pefile.PE(r'client.exe')
  hex(pe.OPTIONAL_HEADER.ImageBase)
  '0x400000'
  ```

