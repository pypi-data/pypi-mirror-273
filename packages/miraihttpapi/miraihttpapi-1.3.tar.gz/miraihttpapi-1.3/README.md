# 快速上手

```python
from miraihttpapi import MiraiCore
from miraihttpapi import MessageChain
with MiraiCore(server_url, verifykey, qqid) as mirai:
    mirai.sendFriendMessage(123456789,MessageChain().plain("Hello"))
```

# 配置文件创建和导入

使用`miraihttpapi.Configer.create(path)`创建一个新的配置文件

使用`miraihttpapi.Configer.load(path)`加载一个配置文件并返回一个未连接的miraihttpapi.MiraiCore(支持使用with进行管理)
