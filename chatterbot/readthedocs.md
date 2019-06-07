# ChatterBot
### weixin and qq
- [wxpy](https://vimerzhao.github.io/2017/08/03/20行代码搭建微信聊天机器人)
- qqbot
### input and output flow
- input
- process input
	- logic adapter1
		- 选择最匹配的输入的回答
	- logic adapter2
- return output
### best match adapter
- input匹配算法：levenshtein来温斯坦距离，就是从一个字符串变成另一个字符串所需要的转变数值，使用dp实现
- 评分算法：
### time logic adapter
- 
### preprocessor
- clean_whitespace将所有的\r或\n或\t或者leading的空格或者tailing的空格替换成"", 所有的多个连续“ ”替换成单个“ ”
### Naive Bayes Classifiers [朴素贝叶斯分类器](http://www.ruanyifeng.com/blog/2013/12/naive_bayes_classifier.html)
- 假设某个体有n项特征（Feature），分别为F1、F2、...、Fn。现有m个类别（Category），分别为C1、C2、...、Cm。贝叶斯分类器就是计算出概率最大的那个分类。
- 可以看一下nltk的naivebayes源码，python的源码应该是最好看的，源码即注释。最后一步是通过归一化来的