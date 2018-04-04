# 美术资源检索系统
- 美术资源检索系统包含：美术资源检索、美术资源版本提交查看和美术资源版本对比等功能
- 系统通过解析美术资源文本类文件的方式，建立美术资源间的关联关系
- 系统还存在许多可以优化和改进的地方
# pip install
- dpath 用于python字典的搜索功能。比较通用的搜索方式，比较慢
- websocket 增加django socket的通信功能，从而向客户端刷新服务器的处理状态

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
│  │  excel_search.html 展示在excel中查找关键词后的查询结果，以iframe的形式嵌套在d3tree.html中
│  │  fulldiff.html
│  │  model_tree.json 当用户请求文件树的时候，将tree下的json文件copy进这个文件中，其实没有必要
│  │  search.html 对原有的index美术资源搜索页面进行了包装，使得能够嵌入现在的系统中
│  │  version_diff.html 美术资源版本对比
│  │  version_list.html 美术资源版本查看
│  │  
│  └─include
│          header.html 网页中包含的js和css文件引用
│          loading.html 网页中loading部分的组件
│          menu.html 公共菜单配置
│          navbar.html 导航条部分，手动更新功能的前端部分
│          
├─utils
│      comm_tools.py 某些公共的tools
│      filename_retriever.py 较慢的搜索方法
│      search_test.py 改进后的搜索方法，目前采用的搜索方法
│      svn_tools.py svn 版本对比和日志查看等功能
│      
└─web
        base.py web controller基类
        version_diff.py 提供version_diff路由的所有功能，其中手动更新索引文件采用websocket通信的方式提供。
        version_list.py 提供version_list路由的所有功能
```

# 功能与实现
- 手动更新索引功能
	- 更新主要包括对美术资源文件进行索引和对excel文件进行索引
	- 美术资源的索引由sync_res.sh完成，对excel文件的索引主要由updateSrc.py完成
	- 美术资源在/home/qcpub/g94_art目录中，excel文件在/home/qcpub/myart/myart/data/xlsx/g94_xlsxdata/目录中
	- 美术资源的索引文件在/home/qcpub/myart/myart/data/resdata目录中，excel文件的索引文件在/home/qcpub/myart/myart/data/excel_pydata目录中
	- 更新excel文件的索引主要通过/home/david/xlsx_search/genXlsData.py文件实现，需要在/home/david/xlsx_search/myweb/data文件下建立指向/home/qcpub/myart/myart/data/xlsx/g94_xlsxdata/目录的xlsdata软链接和指向/home/qcpub/myart/myart/data/excel_pydata目录的pydata软链接，并且将/home/qcpub/myart/myart/data/excel_pydata目录权限修改成777
	- 自动更新索引的crontab文件为crontab_updateSrc.sh
- excel文件检索与索引
	- 项目地址http://192.168.45.130:50000/david/xlsx_search.git
	- 主要在原有项目的基础上增加了genXlsData.py文件完成检索和索引

# 可能遇到的坑
- websocket
	- 1. 嵌入的websocket模块在运行时发生错误不会将真实的报错信息打印在日志中，只会跑出Bad file descriptor的错误。所以只能采用打印调试的方式查找错误
	- 2. 无论websocket是否运行是否出错都会跑出Exception，可以通过http长连接的方式替换掉这部分功能
- angularjs
	- 1. version_diff.html version_list.html代码中使用了大量的ng-repeat，如果不进行分页会导致卡顿
	- 2. 网页中对资源的命名由于一开始开发考量不足，导致可能出现命名重叠而在展开树形图等发生错误
	- 3. 不熟悉ng-repeat作用域的话$index的作用域将会是一个大坑
- 更新锁
	- 更新过程中发生错误时，会导致更新锁仍然存在需要手动删除此锁文件
- 权限问题
	- 对sync_res.sh更新后可能会失去可执行权限，这将导致手动更新功能出错
	- 虽然excel文件和索引都在/home/qcpub下，但是运行的脚本实际在/home/david/xlsx_search/genXlsData.py中，执行时david用户访问qcpub用户的文件会产生权限问题

# 主要功能函数
### 前端
- 1. 初始数据主要是有在请求页面时完成的 
```javascript
var data = {{data | safe}};
```
- 2. angularjs的主要代码需要写在app.controller中
- 3. 分页使用angularjs实现相关函数
```javascript
//初始化
var paginationInit = function(viewby, totalItems)
//设置页码
$scope.setPage = function (pageNo)
//用户选择页码触发函数
$scope.pageChanged = function()

```
- 4. 在下发弹出文件关联树的collapse方法
```javascript
//这里需要改变table的css实现
$scope.collapseBtnClick = function(index) {
	$("#collapse_trigger" + index).click();
	if ($("#td_collapse" + index).hasClass('borderClass')) {
		$("#td_collapse" + index).removeClass('borderClass');
	} else {
		$("#td_collapse" + index).addClass('borderClass')
	}
};
/*
较为复杂的函数
这里是一个二级树的展开函数，涉及到数据请求部分和树的展开
传入的参数主要是为了标识collapse按钮所在位置，因为ng-repeat语句太多了
*/
$scope.collapseTree = function(id, realIndex, type, index, filename)
```
- 5. 公共函数
```javascript
//url: 数据请求的url，data：数据，successFunc：请求成功执行的函数，failFunc：请求失败执行的函数
var myPost = function(url, data, successFunc, failFunc);
//进度条控制函数
startLoading(); closeLoading();
//比alert好看些的弹窗函数使用artDialog实现
var myAlert = function(title, msg)
```
### 后端
- 1. xxx
- 2. xxx

