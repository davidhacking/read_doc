### lucene文件
- index -> segment -> document -> field -> term
- 正向信息文件
	- segments_5(每个索引中有5个段，每个段中有多少个文档), 
	- _1.fnm(对于第1个段有多少个域，每个域的名称，索引方式), 
	- XXX.fdx, XXX.fdt(某个段中的所有文档，每个文档的所有域信息), 
	- XXX.tvx, XXX.tvd, XXX,tvf(所有的词信息)
- 反向信息
	- XXX.tis, XXX.tii 词典
	- XXX.frq term -> document
	- XXX.prx term -> term in document position
### 优化存储的方法 如何实现？
- 词典的存储优化，后面的词存储前面的词的偏移量
- 词在文档中的偏移量存储，后存储的偏移量是前一个词的偏移量的delta，当数值非常大的时候可以节省存储空间