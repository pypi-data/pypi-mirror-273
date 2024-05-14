# 用于存放配置文件
# 使用miraihttpapi.Configer.create(path)创建一个新的配置文件
# 使用miraihttpapi.Configer.load(path)加载一个配置文件并返回一个未连接的miraihttpapi.MiraiCore

from .MiraiCore import MiraiCore
import yaml


def load(config_path:str):
    with open(config_path,encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return MiraiCore(
            server_url=data["server_url"],
            verifykey=data["verifykey"],
            qqid=data["qqid"]

        )

def create(config_path:str):
    with open(config_path,"w+",encoding='utf-8') as f:
        f.write("""#
# 自定义快捷配置文件
# 使用miraihttpapi.Configer.create(path)创建一个新的配置文件
# 使用miraihttpapi.Configer.load(path)加载一个配置文件并返回一个未连接的miraihttpapi.MiraiCore
#


# 服务器地址
server_url: example.com:80
# 验证密匙
verifykey: exampleverifykey
# 绑定QQ号
qqid: 123456789""")