

# ETCyouhui

仿照[廖雪峰的python3实战](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432170937506ecfb2f6adf8e4757939732f3e32b781c000)，建立一个网站。a  web about ETCyouhui

[web app定义](https://en.wikipedia.org/wiki/Web_application)：web app ，即web application，是一种客服端—服务器端的软件程序，其中的用户界面可以在网页浏览器中运行。



## Day 1 搭建开发环境20170814

### 1.确认python版本

在cmd里输入

```
python --version
```

出现

![image](https://user-images.githubusercontent.com/19257507/29265871-3a7af7d8-8115-11e7-9d8b-66ab0ed5ddc1.png)

### 2.利用pip安装Web App的第三方库

> pip，包管理器，一个Python的软件包管理工具，主要是用于安装PyPI上的软件包，用于替代easy_install工具。
>
> PyPI，全称 Python Package Index，是Python的第三方软件资源库。

#### 2.1安装aiohtttp

> `asyncio`可以实现单线程并发IO操作
>
> `asyncio`实现了TCP、UDP、SSL等协议，`aiohttp`则是基于`asyncio`实现的HTTP框架。

在cmd里输入

```
pip install aiohttp
```

#### 2.2 安装前端模板引擎jinjia2

> Jinja是基于python的模板引擎，

在cmd里输入：

```
pip install jinja2
```

#### 2.3 MySQL5.x数据库

在[MySQL官方网站](https://dev.mysql.com/downloads/mysql/5.6.html)上下载MySQL，下载并安装。

我的MySQL的用户名是：root

口令是：test123

安装MySQL的异步驱动程序aiomysql，在cmd里输入

```
pip install aiomysql
```

注：因为我没有安装python2，只有python3版本，所以不用在cmd里命令行里写成python3和pip3

### 3.建立文件夹

参照廖雪峰的文件结构，建立文件夹如下。

```
ETCyouhui/   <--根目录
|
+— backup/   <--备份目录
|
+— conf/     <--配置文件
|
+— dist/     <--打包目录
|
+— www/      <--Web目录，存放.py文件
|  |
|  +—static/ <-- 存放静态文件，即CSS框架
|  |
|  +—templates/ <--存放模板文件，即.html文件。
|
+— ios/         <--存放iOS App工程
|
+— LICENSE      <--代码LICENSE,授权。
```

### 4.同步到github



### 5.开发工具

廖雪峰推荐Sublime Text。

我使用是*JetBrains PyCharm Community Edition 2016.2.3*



### Day2 编写 Web App骨架

#### 1.常识

> [asyncio：](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432090954004980bd351f2cd4cc18c9e6c06d855c498000)是Python3.4版本引入的标准库，直接内置了对异步IO的支持。asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。`asyncio`可以实现单线程并发IO操作。如果把`asyncio`用在服务器端，例如Web服务器，由于HTTP连接就是IO操作，因此可以用单线程+`coroutine`实现多用户的高并发支持。

> `asyncio`实现了TCP、UDP、SSL等协议，`aiohttp`则是基于`asyncio`实现的HTTP框架。

#### 2.编写

编写Web App骨架就是再www的文件夹下写一个app.py。



### Day3 编写ORM

#### 1.常识

> ORM，即[**Object Relational Mapping**](https://baike.baidu.com/item/ORM)，意思是对象关系映射，把数据表的行与相应的对象建立关联，互相转换，把关系数据库的表结构映射到对象上。
>
> ORM，用来把对象模型表示的对象映射到基于S Q L 的关系模型数据库结构中去。这样，我们在具体的操作实体对象的时候，就不需要再去和复杂的 SQ L 语句打交道，只需简单的操作实体对象的属性和方法。

##### 2.示例

创建一个orm，并插入一个数字

```
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

Base = declarative_base()

class User(Base):
    __tablename__='user'
    id= Column(String(20),primary_key=True)
    name=Column(String(20))

engine= create_engine('mysql+pymysql://root:test123@localhost:3306/test')
DBSession =sessionmaker(bind=engine)

session =DBSession()
new_user=User(id='10',name='123')
session.add(new_user)
session.commit()
session.close()
```

#### 3.操作

> 在Web App中，包括用户信息、发布的日志、评论等数据，都存在SQL中。
>
> 利用ORM，封装和数据库关联的函数，比如SELECT，INSERT，UPDATE 和DELETE。

（1）创建连接池，`def create_pool(loop, **kw):`

（2）创建select函数，执行SELECT语句，`def select(sql, args, size=None):`

（3）创建execute函数，执行INSERT，UPDATE，DELETE语句，`def execute(sql, args):`

（4）编写ORM。

- 首先从调用者角度设计，定义一个和数据库表users关联的User对象。`class User(Model):`


（5）定义Model类，方便ORM映射。

（6）定义Field类，和各种子类，StringField，BooleanField，IntegerField，FloatField，TextField

（7）定义ModelMetaclass类，让Model的子类读取映射信息。

（8）在Model类中定义class 方法，让子类调用class方法，

```
@classmethod
async def find(cls,pk):
		代码块
```

（9）在Model类中添加实例方法，可以让子类调用

```
 async def save(self):
    	代码块
 
 async def update(self):
        代码块
 
 async def remove(self):
 		代码块        
```

（10）在Model中，定义sql的查找方法

```
@classmethod
async  def findALL(cls, where =None, args= None, **kw):
		代码块
@classmethod
async def findNumber(cls, selectField, where=None, args=None):
		代码块
```



### Day4 编写Model

#### 1.常识

在www文件下编写Model.py文件

#### 2.操作

（1）定义3个表，User表，Blog表，和Comment表

```
class User(Model):
class Blog(Model):
class Comment(Model):
```

（2）初始化数据库表

在www文件下编辑一个.sql文件，命名为schema.sql

在cmd命令行里进入mysql文件下bin文件下。执行

```
mysql -u root -ptest123<d:ETCyouhui\www\schema.sql
```

则自动在Mysql数据库里创建ETCyouhui库，在库里创建User表，Blog表，和Comment表，并定义好字段。

（3）编写数据访问代码

定义user为

```
  u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
```





### Day5 编写Web框架

#### 1.原因

因为aiohttp比较低级，所以要重新封装一个web框架。

建立了三个文件，

（1）apis.py（定义JSON API）

（2）coroweb.py（放web框架）

（3）handlers.py（处理URL函数）

（4）修改app.py文件

#### 2.步骤

##### 2.1定义@get() 和 @post()。在www文件夹下，建立coroweb.py文件。

>一个函数通过`@get()`的装饰就附带了URL信息。

##### 2.2定义RequestHandler。在coroweb.py文件里编写。

（1）定义RequestHandler()

> 用`RequestHandler()`来封装一个URL处理函数
>
> RequestHandler()目的就是从URL函数中分析其需要接收的参数，从`request`中获取必要的参数，调用URL函数，然后把结果转换为`web.Response`对象，这样，就完全符合`aiohttp`框架的要求。

（2）编写`add_route`函数，用于注册一个URL处理函数

（3）编写`add_routes`函数，把多次的add_route()注册的调用变成自动扫描

##### 2.3在文件`app.py`中加入`middleware`、`jinja2`模板和自注册的支持

###### 2.3.1  定义`inint_jinja2`

###### 2.3.2  定义 middleware

制作拦截器middleware，在app.py文件里。URL在被某个函数处理前，要经过一系列的middleware的处理。

> middleware可以改变URL的输入、输出，甚至可以决定不继续处理而直接返回。middleware的用处就在于把通用的功能从每个URL处理函数中拿出来，集中放到一个地方。

middleware包括定义

（1）`logger_factory()`:记录URL日志

（2）`data_factory()`

（3）`response_factory()`:把返回值转换为`web.Response`对象再返回，以保证满足`aiohttp`的要求。

（4）`datetime_filter()`

##### 2.4 新建handlers.py文件





### Day6  编写配置文件

#### 1.原理

###### 1.1 装配APP

> 一个Web APP在运行时需要读取配置文件，比如数据库的用户名，口令。

可以直接用python代码实现配置

##### 1.2 应用文件

config_default.py ( 默认的配置文件，开发环境的标准配置)

config_override.py (生产环境的标准配置，覆盖某些默认配置，比如数据库的host等信息，应用程序优先从这个文件中读取)

config.py    （简化读取配置文件，将所有配置读取到该文件中）





### Day7 编写MVC

#### 1.原理

##### 1.1 什么是MVC

[MVC](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014320129740415df73bf8f81e478982bf4d5c8aa3817a000)，即 Model-View-Controller，模型—视图—控制器

> C：即负责处理URL的函数，负责业务逻辑，比如 用户名是否存在，取出用户信息等，
>
> V:  即包含变量{{name}}的模板，负责 显示逻辑，替换变量，输出用户可以看到的HTML
>
> M：用来传给View，view在替换变量时，可以从Model中取出相应的数据。

##### 1.2应用文件

www文件夹下的handlers.py（处理首页URL）

mysql 数据库的awesome库的users表(添加用户信息)

templates文件夹下的test.html（模板）

#### 2.操作步骤

1.www文件夹下handlers.py文件，编写@get。

2.在mysql 数据库的awesome库的users表里写上数据

![image](https://user-images.githubusercontent.com/19257507/29662622-909b6eda-88fa-11e7-9fb4-2dab51d02931.png)

​             



![20170807155309](D:\python2017\sql\20170807155309.png)

3.要在templates文件夹里建立test.html。





### Day8 构建前端

#### 1.原理

##### 1.1 CSS框架。

**可以从[uikit首页](http://getuikit.com/)下载打包的资源文件**，由于uikit版本更新，且文件数目和名称不一致，我直接从廖雪峰的githuba里下载的，复制粘贴。

##### 1.2 应用文件

（1） handlers.py文件（修改首页URL的处理函数）。

（2）app.py（修改filter）。

#### 2.操作步骤

##### 2.1 建立CSS框架

（1）从uikit下载，放到www/static文件夹下。建立的文件结构如下

```
static/
+-css\
|    +—addons\
| 	 | 	+—uikit.addons.min.css
| 	 | 	+—uikit.almost-flat.addons.min.css
| 	 | 	+—uikit.gradient.addons.min.css
|    +—awesome.css
|    +—uikit.almost-flat.min.css
|    +—uikit.gradient.min.css
|    +—uikit.min.css|
+—fonts\
|	+—FontAwesome.otf
|	+—fontawesome-webfont.eot
|	+—fontawesome-webfont.ttf
|	+—fontawesome-webfont.woff
+—img\
|   +—user.png
+—js\
    +—awesome.js
    +—jquery.min.js
    +—sha1.min.js
    +—sticky.min.js
    +—uikit.min.js
    +—vue.min.js
```

##### 2.2 页面模板复用问题

###### 2.2.1问题：

页面的页眉页脚需要保持一致，实现模板复用。

######2.2.2方法：

jinjia2可以通过**继承**方式，实现模板复用

######2.2.3步骤：

（1）写一个父模板`base.html`，定义可替换的block(块)

```
{% block title%}....{% endblock %}
{% block content%}...{% endblock %}
{% block beforehead %}...{% endblock %}
{% block meta %}...{% endblock meta%}

```

（2）编写子模板，只替换父模板的block

```
{%extends 'base.html' %}
{% block title %} A {% endblock %} 
{% block content %} ....{% endblock %} 
```

##### 2.3 修改处理首页URL的函数

**首页URL的处理函数**是在handlers.py文件里修改。

##### 2.4 将Blog创建日期的浮点数改为日期字符串

通过jinjia2的filter（过滤器）修改，定义`datatime_filter` ，在app.py里修改。

##### 2.5其他

在`app.py`里加上`from config import configs` 。

网页中的文章名称`Test Blog` ， `Something New`， `Lerarn Swift` 和文章内容是在handlers.py中被定义的。



### DAY 9 编写API 

#### 1.原理

##### 1.1 REST

Web服务实现方案有三种：SOAP 、XML-RPC和REST。

[REST](https://zh.wikipedia.org/wiki/REST)，Representational State Transfer，具象状态传输，属于万维网软件架构的一种风格，模式简洁。

> REST就是一种设计API的模式。最常用的数据格式是JSON。由于JSON能直接被JavaScript读取，所以，以JSON格式编写的REST风格的API具有简单、易读、易用的特点。

##### 1.2 Web API

[API](http://baike.baidu.com/link?url=_paVM0N8dpo3aTcGOzPFJVjlKs_H52P0IeMdxn90V7bjr13ZuI3h8NS-N7uq6hNxz6gDi-1m7mK-wrQEVeeTWa)，Application Programming Interface，应用程序编程接口

> 如果一个URL返回的不是HTML，而是机器能直接解析的数据，这个URL就可以看成是一个Web API。

> 编写API有什么好处呢？由于API就是把Web App的功能全部封装了，所以，通过API操作数据，可以极大地把前端和后端的代码隔离，使得后端代码易于测试，前端代码编写更简单。

> 一个API也是一个URL的处理函数，我们希望能直接通过一个`@api`来把函数变成JSON格式的REST API。

##### 1.3 应用文件

handlers.py（增加用户注册API）

#### 2.操作步骤

##### 2.1 实现用户注册的API

在handlers.py里增加`def api_get_users(*, page='1'):`。



### Day10-用户注册和登录

#### 1.原理

##### 1.1 原理

（1）API实现用户注册功能

（2）创建注册页面

（3）实现用户登录功能：使用Session功能封装保护用户状态的cooke。

> [cookie](https://baike.baidu.com/item/cookie/1119?fr=aladdin),储存在用户本地终端上的数据。

> [Session](https://baike.baidu.com/item/session/479100?fr=aladdin)，会话控制，Session 对象存储特定用户会话所需的属性及配置信息。这样，当用户在应用程序的 Web 页之间跳转时，存储在 Session 对象中的变量将不会丢失，而是在整个用户会话中一直存在下去。当用户请求来自应用程序的 Web 页时，如果该用户还没有会话，则 Web 服务器将自动创建一个 Session 对象。当会话过期或被放弃后，服务器将终止该会话。Session 对象最常见的一个用法就是存储用户的首选项。

> Session的优点是简单易用，可以直接从Session中取出用户登录信息。

> Session的缺点是服务器需要在内存中维护一个映射表来存储用户登录信息，如果有两台以上服务器，就需要对Session做集群，因此，使用Session的Web App很难扩展。
>
> 由于登录成功后是由服务器生成一个cookie发送给浏览器，所以，要保证这个cookie不会被客户端伪造出来。

> [SHA1](https://baike.baidu.com/item/SHA1/8812671?fr=aladdin)，安全[哈希算法](https://baike.baidu.com/item/%E5%93%88%E5%B8%8C%E7%AE%97%E6%B3%95)（Secure Hash Algorithm）主要适用于[数字签名](https://baike.baidu.com/item/%E6%95%B0%E5%AD%97%E7%AD%BE%E5%90%8D)标准 （Digital Signature Standard DSS）里面定义的数字签名算法（Digital Signature Algorithm DSA）

> 实现防伪造cookie的关键是通过一个单向算法（例如SHA1）,SHA1是一种单向算法，即可以通过原始字符串计算出SHA1结果，但无法通过SHA1结果反推出原始字符串。

> 用户输入正确用户名和密码，登录成功后，服务器可以从数据库渠道用户的id，并计算出一个字符串

> `"用户id" + "过期时间" + SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey"`

> 浏览器发送cookie到服务器后，服务器可以获得`"用户id" + "过期时间" + SHA1值` ，如果未到过期时间，服务器可以根据用户id查找用户口令，计算`SHA1("用户id" + "用户口令" + "过期时间" + "SecretKey")`, 并将SHA1值与浏览器cookie中的MD5比较，如果相等，则说明用户已登录，否则，cookie就是伪造。

##### 

##### 1.2 应用文件

1. 通过API实现用户注册功能，代码是写在handlers.py文件里。

2. 在templates文件夹里编写register.html（用户注册页面）和signin.html（用户登录页面）文件。

3. app.py文件需要加一行`from handlers import cookie2user, COOKIE_NAME`

   ```
   @asyncio.coroutine
   def auth_factory(app, handler):
   ```

   ​

4. handlers.py里增加

   ```
   import markdown2
   from aiohttp import web
   from apis import APIValueError, APIResourceNotFoundError
   from config import configs
   COOKIE_NAME = 'awesession'
   _COOKIE_KEY = configs.session.secret

   def user2cookie(user, max_age):
   ......
   @asyncio.coroutine
   def cookie2user(cookie_str):
   .......

   @get('/')
   def index(request):
   ......

   @get('/register')
   def register():
   .......
   @get('/signin')
   def signin():
   .......
   @post('/api/authenticate')
   def authenticate(*, email, passwd):
   .......
   @get('/signout')
   def signout(request):
   ......
   _RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
   _RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

   #修改def api_register_user
   @post('/api/users')
   def api_register_user(*, email, name, passwd):
   ```

   5. 在www文件夹下增加markdown2.py



#### 2.操作步骤

##### 2.1实现用户注册功能

在handlers.py里增加

```
@post('/api/users')
def api_register_user(*, email, name, passwd):
....等等
```

##### 2.2创建用户注册页面

可以让用户填写注册表单，然后，提交数据到用户注册的API。

在templates文件夹里编写register.html。

##### 2.3 实现用户登录功能

在handlers.py里增加

```
@post('/api/authenticate')
def authenticate(*, email, passwd):
.....

# 计算加密cookie:
def user2cookie(user, max_age):
```

为不用重复写解析cookie的代码，可以在middle处理URL之前，把cookie解析处理，并登录用于绑到request对象上。

在app.py里增加

```
@asyncio.coroutine
def auth_factory(app, handler):

```

在handlers.py里增加

```

@asyncio.coroutine
def cookie2user(cookie_str):
.....
```

##### 2.4 编写用户登录页面

在templates文件夹里编写signin.html。



#### 3.结果

成功注册并登录，哈哈哈！

用户名：bruce@163.com

密码：123456



### Day11-编写日志创建页

#### 1.原理

#### 1.1实现日志创建

编写REST API，创建一个Blog。

#### 1.2 MVVM

[MVVM模式](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)，即[Model View ViewModel模式](https://baike.baidu.com/item/MVVM/96310?fr=aladdin)。

> MVVM是Model-View-ViewModel的简写。微软的WPF带来了新的技术体验，如Silverlight、[音频](https://baike.baidu.com/item/%E9%9F%B3%E9%A2%91)、[视频](https://baike.baidu.com/item/%E8%A7%86%E9%A2%91)、[3D](https://baike.baidu.com/item/3D/25017)、[动画](https://baike.baidu.com/item/%E5%8A%A8%E7%94%BB)……，这导致了软件UI层更加细节化、可定制化。同时，在技术层面，WPF也带来了 诸如Binding、Dependency Property、Routed Events、Command、DataTemplate、ControlTemplate等新特性。MVVM（Model-View-ViewModel）框架的由来便是MVP（Model-View-Presenter）[模式](https://baike.baidu.com/item/%E6%A8%A1%E5%BC%8F/700029)与WPF结合的应用方式时发展演变过来的一种新型架构[框架](https://baike.baidu.com/item/%E6%A1%86%E6%9E%B6)。

> 前端页面中，用JavaScript对象表示Model，Model表示数据。
>
> 用HTML表示View，View负责表示
>
> ViewModel负责关联Model和View，把Model的数据同步到View，进行显示，再把View的修改同步返回Model。
>
> ViewModel的编写工具：JavaScript
>
> MVVM框架：AngularJS，KnockoutJs等，这里使用[Vue框架](https://vuejs.org/)。

##### 1.2应用文件

（1）apis.py文件

（2）handlers.py文件

（3）manage_blog_edit.html文件

（4）app.py文件修改

#### 2.操作步骤

（1）apis.py文件里

- 需要定义class Page，
- 最后面需要加上

```
if __name__=='__main__':
    import doctest
    doctest.testmod() 
```

（2）在handlers.py里加上

```
def check_admin(request):
....

def get_page_index(page_str):
.....

def text2html(text):
.....

@get('/blog/{id}')
def get_blog(id):
.....

@post('/api/blogs')
def api_create_blog(request,*,name,summary,content):
	代码块

@get('/api/blogs/{id}')
def api_get_blog(*, id):
.....

@post('/api/blogs')
def api_create_blog(request, *, name, summary, content):
.....
```

（3）在templates文件夹里创建manage_blog_edit.html文件（使用Vue框架）。

（4）app.py文件修改

```
@asyncio.coroutine
def init(loop):
```

#### 4.关键点

4.1 app.py文件里的`async def init(loop):`函数里要加上要加上auth_factory, 

```
app = web.Application(loop=loop, middlewares=[
        logger_factory,auth_factory, response_factory
    ])
```

4.2 app.py文件里的`async def init(loop):`函数里写成：

```
yield from orm.create_pool(loop=loop, **configs.db)
```

会报错连接不上数据库，还是写成

```
await orm.create_pool(loop=loop, host='127.0.0.1', port=3306, user='root', password='test123', db='etcyouhui')
```

不会出错

4.3 登录后总是返回原来界面，无法进入编辑界面

（1）修改app.py文件里的`def authfactory(app, handler):`

`if request.path.startswith('/manage/') and (request.\**user** is None or not request._user*.admin):            return web.HTTPFound('/signin')`

中的` not request.**user**.admin `去掉not， 因为在注册用户时，默认的admin值是False （0）.

（2）修改handlers.py文件里的的

```
def check admin(request):
    if request.user is None or not request._user.admin:
        raise APIPermissionError()

```

去掉`not request._user.admin`中的not。





### Day12-编写日志列表页

#### 1.原理

##### 1.1 实现管理页面

利用MVVM模式，实现管理页面

##### 1.2应用文件

（1）handlers.py（实现API）

```
@get('/api/blogs')
def api_blogs(*, page='1'):
....
```

​      定义管理页面

```
@get('/manage/blogs')
def manage_blogs(*, page='1'):
```

（2）在templates里建立manage_blogs.html文件

#### 2.操作步骤

##### 2.1在handlers.py中实现API

```
@get('/api/blogs')
def api_blogs(*,page='1'):
	代码块
```

##### 定义管理页面

```
@get('/manage/blogs')
def manage_blogs(*,page='1'):
	代码块
```

`from apis`里加上`Page`

```
from apis import Page,APIValueError, APIResourceNotFoundError
```

##### 2.2 在templates里建立manage_blogs.html文件，即所谓的**模板管理页面**。



#### Day 13-提升开发效率（实现自动修改代码的加载）

#### 1.原理

##### 1.1问题

每次修改代码，都必须先停止服务器，再重启，改动才能生效。

##### 1.2目的

实现服务器检测到代码修改后自动重新加载。

##### 1.3方法

监测www目录下的代码改动，一旦改动，就重启服务器。

> 在www的文件夹里建立pymonitor.py文件，可以启动 wsgiapp.py进程，监控www目录下的代码改动，有改动，就停止 wsgiapp.py进程，再重启，相当于完成了服务器进程的自动重启。

Python第三方库watchdog可以利用操作系统的API监控目录文件的变化，并发送通知。

利用Python自带的subprocess可以实现进程的启动和终止，并把输入输出定向到当前进程的输入输出中

##### 1.4应用文件

在www的文件夹里建立pymonitor.py文件。

#### 2.步骤

##### 2.1安装watchdog

在命令行里`pip install wathcdog`

##### 2.2编写pymonitor.py文件

在www的文件夹里建立pymonitor.py文件。

pymonitor.py文件里 `python3`改成`python`。

```
  if argv[0] != 'python':
        argv.insert(0, 'python')
```

##### 2.3运行pymonitor.py文件

在cmd里`python pymonitor.py app.py`



#### Day 14-完成Web App

#### 1.原理

##### 1.1目的

在Debug模式下，完成后端所有API，前端的所有页面。

##### 1.2具体方法

（1）把当前用户绑定到`request`上，并对URL`/manage/`进行拦截，检查用户是否是管理员身份

```
@asyncio.coroutine
def auth_factory(app, handler):
```

（2）后端API包括：(在handlers.py里修改)

- 获取日志：GET /api/blogs
- 创建日志：POST /api/blogs
- 修改日志：POST /api/blogs/:blog_id
- 删除日志：POST /api/blogs/:blog_id/delete
- 获取评论：GET /api/comments
- 创建评论：POST /api/blogs/:blog_id/comments
- 删除评论：POST /api/comments/:comment_id/delete
- 创建新用户：POST /api/users
- 获取用户：GET /api/users

（3）管理页面包括：(在handlers.py里修改)

- 评论列表页：GET /manage/comments
- 日志列表页：GET /manage/blogs
- 创建日志页：GET /manage/blogs/create
- 修改日志页：GET /manage/blogs/
- 用户列表页：GET /manage/users

（4）用户浏览页面包括：

- 注册页：GET /register
- 登录页：GET /signin
- 注销页：GET /signout
- 首页：GET /
- 日志详情页：GET /blog/:blog_id

#### 2.步骤

##### 2.1  在app.py文件里的第55行加上。（Day 10 中已加）

```
@asyncio.coroutine
def auth_factory(app, handler):
		代码块
```

##### 2.2  后端API是在handlers.py文件里编写的。

（1）第79行`def index()`修改

（2）第 151行增加多个函数：

```
@get('/manage/')
def manage():
```

```
@get('/manage/comments')
def manage_comments(*, page='1'):
```

```
@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
```

```
@get('/manage/users')
def manage_users(*, page='1'):
```

```
@get('/api/comments')
def api_comments(*, page='1'):
```

```
@post('/api/blogs/{id}/comments')
def api_create_comment(id, request, *, content):
```

```
@post('/api/comments/{id}/delete')
def api_delete_comments(id, request):
```

```
@get('/api/users')
def api_get_users(*, page='1'):
```

(3) 第291行加上两个函数：

```
@post('/api/blogs/{id}')
def api_update_blog(id, request, *, name, summary, content):
```

```
@post('/api/blogs/{id}/delete')
def api_delete_blog(request, *, id):
```

##### 2.3  hanadlers.py文件，第15行加上`,APIError`(DAY 12中已加上)

```
from apis import Page, APIValueError, APIResourceNotFoundError,APIError
```

##### 2.4 在templates文件夹里，添加文件

加上blog.html文件，manage_comments.html文件，manage_users.html文件，

##### 2.5 在templates文件夹里，修改文件

（1）在`manage_blog_edit.html`里，第26行，改为

```
 return location.assign('/manage/blogs');
```



#### 3.关键点

##### 3.1 首页日志翻页

hanadlers.py文件，`def index(*, page='1'):`中，第82行` page = Page(num)`，改为

```
page = Page(num,page_index)
```

##### 3.2 增加登出功能和日志评论按钮

app.py文件中，`def response_factory(app, handler):`函数中，第111行，增加一行

```
r['__user__'] = request.__user__
```

handlers.py文件，`def get_blog(id,request):`参数增加`request`






































引用：

[廖雪峰的python3](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432170937506ecfb2f6adf8e4757939732f3e32b781c000)

[Python包管理工具——Pip](http://blog.csdn.net/olanlanxiari/article/details/48086917)

[Python官网](https://wiki.python.org/moin/CheeseShopTutorial)

[Wiki百科——pip](https://en.wikipedia.org/wiki/Pip_(package_manager))

[Wiki百科——PyPI](https://en.wikipedia.org/wiki/Python_Package_Index)

[Jinja2 简明使用手册](https://www.oschina.net/question/5189_3943)

[ORM](https://baike.baidu.com/item/ORM)