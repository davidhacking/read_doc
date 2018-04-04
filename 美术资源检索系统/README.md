# 美术资源检索系统
- 美术资源检索系统包含：美术资源检索、美术资源版本提交查看和美术资源版本对比等功能
- 系统通过解析美术资源文本类文件的方式，建立美术资源间的关联关系
- 系统还存在许多可以优化和改进的地方
# pip install
- dpath 用于python字典的搜索功能。比较通用的搜索方式，比较慢

# 项目目录
```bash
├─data
│  ├─resdata
│  │      reverse_sceneinfo.py
│  │      reverse_xxxinfo.py
│  │      sceneinfo.py
│  │      search_test.py
│  │      xxxinfo.py
│  │      
│  └─tree
│          character%dongzuoku%base02.gim.json
│          
├─scripts
│      config.py
│      dict2Json.py
│      fxdict.py
│      genRes2Dict.py
│      gim_to_json.py
│      res2dict.py
│      reverse_resdict.py
│      search_utils.py
│      uidict.py
│      
├─templates
│  │  404.html
│  │  base.html
│  │  d3tree.html
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