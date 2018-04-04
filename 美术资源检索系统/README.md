# 美术资源检索系统
- 美术资源检索系统包含：美术资源检索、美术资源版本提交查看和美术资源版本对比等功能
- 系统通过解析美术资源文本类文件的方式，建立美术资源间的关联关系
- 系统还存在许多可以优化和改进的地方
# pip install
- dpath 用于python字典的搜索功能。比较通用的搜索方式，比较慢

# 项目目录
```bash
├─data 存储字典文件
│  ├─resdata
│  │      reverse_sceneinfo.py 
│  │      reverse_xxxinfo.py 对字典文件进行反向索引提高检索速度
│  │      sceneinfo.py scene文件的字典文件，索引方式与一般格式不同，其中key是目录
│  │      search_test.py 用于远程检验检验搜索功能是否有问题
│  │      xxxinfo.py 字典文件，如giminfo.py，格式比较统一
│  │      
│  └─tree
│          character%dongzuoku%base02.gim.json 采用d3tree的json格式存储，从索引文件生成而来，其实可以临时生成
│          
├─scripts
│      config.py 配置文件，本地配置和服务器配置的目录会有区别，提交时需要注意
│      dict2Json.py 将字典文件生成tree下的json文件，采用json配置的方式对每一个需要生成的美术资源文件进行配置生成
│      genRes2Dict.py 将资源文件生成字典文件，同样采用json配置的方式运行，能够生成如csd文件的子树。
│      gim_to_json.py 将字典文件生成tree下的json文件，这是上一个作者的代码，dict2Json.py对此代码进行了重构
│      res2dict.py 功能同genRes2Dict.py，建议需要增加功能时对genRes2Dict.py进行修改即可
│      reverse_resdict.py 建立反向索引
│      search_utils.py 根据文件名对字典文件进行检索，检索结果形式较为复杂，存在可以简化的地方
│      uidict.py
│      
├─templates
│  │  404.html 404功能，需要在django中配置DEBUG=False是可用
│  │  base.html 网页采用django的template的语言配置实现，此为网页的基类
│  │  d3tree.html d3tree在系统的许多地方均有用到，所以采用iframe的方式提供功能，使用时注意阅读iframe的height设置部分，因为经常出现iframe嵌套iframe的情况
│  │  excel_search.html
│  │  fulldiff.html
│  │  model_tree.json
│  │  search.html
│  │  version_diff.html
│  │  version_list.html
│  │  
│  └─include
│          header.html
│          loading.html
│          menu.html
│          navbar.html
│          
├─utils
│      comm_tools.py
│      filename_retriever.py
│      search_test.py
│      svn_tools.py
│      
└─web
        base.py
        version_diff.py
        version_list.py
```