# 用于连接mirai-api-http的http接口
# This function uses json to pass information.
#     Format:
#         {
#             "id": 0~2       // This uses to pass state id
#                 // 0:normal 1:allowed error 2:uncorrectable error
#             "msg": ""       // This uses to pass message information
#                 // For example "Connection succeeded",and this will be able to be printed.
#             "_data": all     // This uses to pass _data information
#         }


from .MessageChain import MessageChain

import requests
import urllib


class MiraiCore(object):
    def __init__(
        self,
        server_url: str,
        verifykey: str,
        qqid: int
    ):
        """
        Init your config , and need:
            server_url  : your server url(e.g. "xxxx.xxx:xxxx")
            verifykey   : the key you set on the server
            qqid        : your bot's qq ID
        """
        self.url = "http://"+str(server_url)
        self.verifykey = str(verifykey)
        self.qqid = int(qqid)
        self.sessionKey = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args, **kwargs):
        self.disconnect()

    def _commandPost(self, cmd: str, content: dict = {}):
        if self.sessionKey:
            content["sessionKey"] = self.sessionKey
        return requests.post(
            self.url+f"/{cmd}?",
            json=content,
            headers={'Content-Type': 'application/json'}
        ).json()

    def _commandGet(self, cmd: str, content: dict = {}):
        content["sessionKey"] = self.sessionKey
        return requests.get(
            self.url+f"/{cmd}?{urllib.parse.urlencode(content)}",
        ).json()

    def verify(self) -> dict:
        """
        This function is used to verify server.
        """
        self.sessionKey = self._commandPost(
            "verify",
            {
                "verifyKey": self.verifykey,
            }
        )["session"]

    def bind(self):
        return self._commandPost(
            "bind",
            {
                "qq": self.qqid,
            }
        )

    def connect(self) -> dict:
        """
        This function is used to connect server and subscribe to messages and event.
        """
        self.verify()
        return self.bind()

    def get(self, num: int = 1) -> dict:
        """
        This function is used to get information from server.
        """
        while True:
            return self._commandGet(
                "fetchMessage",
                {
                    "count": num
                }
            )

    def disconnect(self):
        """
        This function is used to disconnect from server.
        """
        try:
            return self._commandPost(
                "release",
                {
                    "qq": self.qqid
                }
            )
        except:
            return {"id": 1, "msg": "Connection lost"}

    def close(self):
        """
        This function is used to disconnect from server.
        """
        return self.disconnect()

    """
    下面是根据mirai-api-http写的接口，可以直接调用并且有函数注解
    """

    def about(self) -> dict:
        """
        使用此方法获取mirai-api-http插件的信息，如版本号
        """
        return self._commandGet(
            "about"
        )

    def messageFromId(self, message_id: int) -> dict:
        """
        此方法通过messageId获取历史消息,
        """
        return self._commandGet(
            "messageFromId",
            {
                "id": message_id
            }
        )

    def friendList(self) -> dict:
        """
        使用此方法获取bot的好友列表
        """
        return self._commandGet(
            "friendList"
        )

    def groupList(self) -> dict:
        """
        使用此方法获取bot的群列表
        """
        return self._commandGet(
            "groupList"
        )

    def memberList(self, group_id: int) -> dict:
        """
        使用此方法获取bot指定群中的成员列表
        """
        return self._commandGet(
            "memberList",
            {
                "target": group_id
            }
        )

    def botProfile(self) -> dict:
        """
        此接口获取session绑定bot的详细资料
        """
        return self._commandGet(
            "botProfile"
        )

    def friendProfile(self, user_id: int) -> dict:
        """
        此接口获取好友的详细资料
        """
        return self._commandGet(
            "friendProfile",
            {
                "target": user_id
            }
        )

    def memberProfile(self, group_id: int, user_id: int) -> dict:
        """
        此接口获取群成员的消息资料
        """
        return self._commandGet(
            "memberProfile",
            {
                "target": group_id,
                "memberId": user_id
            }
        )

    def sendFriendMessage(self, user_id: int, messageChain: MessageChain) -> dict:
        """
        使用此方法向指定好友发送消息
        """
        return self._commandPost(
            "sendFriendMessage",
            {
                "target": user_id,
                "messageChain": messageChain.get()
            }
        )

    def sendGroupMessage(self, group_id: int, messageChain: MessageChain) -> dict:
        """
        发送群消息
        """
        return self._commandPost(
            "sendGroupMessage",
            {
                "target": group_id,
                "messageChain": messageChain.get()
            }
        )

    def sendTempMessage(self, user_id: int, group_id: int, messageChain: MessageChain) -> dict:
        """
        发送临时会话消息
        """
        return self._commandPost(
            "sendTempMessage",
            {
                "qq": user_id,
                "group": group_id,
                "messageChain": messageChain.get()
            }
        )

    def sendNudge(self, target: int, subject: int, kind: str) -> dict:
        """
        发送头像戳一戳消息
            target:目标id
            subject:目标子id(例如群号，或者QQ号)
            kind:"Group" or "Friend" or "Stranger"
        """
        return self._commandPost(
            "sendNudge",
            {
                "target": target,
                "subject": subject,
                "kind": kind
            }
        )

    def recall(self, messageId: int) -> dict:
        """
        撤回消息
        """
        return self._commandPost(
            "recall",
            {
                "target": messageId
            }
        )

    def file_list(self, target_id: int, path_id: str = "") -> dict:
        """
        查看文件列表
        """
        return self._commandGet(
            "file/list",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "withDownloadInfo": False,
                "offset": 0,
                "size": 1
            }
        )

    def file_info(self, target_id: int, path_id: str) -> dict:
        """
        获取文件信息
        """
        return self._commandGet(
            "file/info",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "withDownloadInfo": True
            }
        )

    def file_mkdir(self, target_id: int, path_id: str, directoryName: str = "New Folder") -> dict:
        """
        创建文件夹
        """
        return self._commandPost(
            "file/mkdir",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "directoryName": directoryName
            }
        )

    def file_delete(self, target_id: int, path_id: str) -> dict:
        """
        删除文件
        """
        return self._commandPost(
            "file/delete",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None
            }
        )

    def file_move(self, target_id: int, path_id: str, move_path_id: str) -> dict:
        """
        移动文件
        """
        return self._commandPost(
            "file/move",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "moveTo": move_path_id,
                "moveToPath": None
            }
        )

    def file_rename(self, target_id: int, path_id: str, name: str) -> dict:
        """
        重命名文件
        """
        return self._commandPost(
            "file_rename",
            {
                "id": path_id,
                "path": None,
                "target": target_id,
                "group": None,
                "qq": None,
                "renameTo": name
            }
        )

    def file_upload(self, group_id: int, file_path: str, file_name) -> dict:
        """
        群文件上传(以服务器目录为准)
        """
        return self._commandPost(
            "file/upload",
            {
                "type": "group",
                "target": group_id,
                "path": file_path,
                "file": file_name,
            }
        )

    def deleteFriend(self, user_id) -> dict:
        """
        删除好友
        """
        return self._commandPost(
            "deleteFriend",
            {
                "target": user_id
            }
        )

    def mute(self, group_id: int, user_id: int, set_time: int = 600) -> dict:
        """
        禁言群成员
        """
        return self._commandPost(
            "mute",
            {
                "target": group_id,
                "memberId": user_id,
                "time": set_time
            }
        )

    def unmute(self, group_id: int, user_id: int) -> dict:
        """
        解除群成员禁言
        """
        return self._commandPost(
            "unmute",
            {
                "target": group_id,
                "memberId": user_id
            }
        )

    def kick(self, group_id: int, user_id: int, msg: str = "您已被移出群聊") -> dict:
        """
        移除群成员
        """
        return self._commandPost(
            "kick",
            {
                "target": group_id,
                "memberId": user_id,
                "msg": msg
            }
        )

    def quit(self, group_id: int) -> dict:
        """
        退出群聊
        """
        return self._commandPost(
            "quit",
            {
                "target": group_id
            }
        )

    def muteAll(self, group_id: int) -> dict:
        """
        全体禁言
        """
        return self._commandPost(
            "muteAll",
            {
                "target": group_id
            }
        )

    def unmuteAll(self, group_id: int) -> dict:
        """
        解除全体禁言
        """
        return self._commandPost(
            "unmuteAll",
            {
                "target": group_id
            }
        )

    def setEssence(self, messageId: int) -> dict:
        """
        设置群精华消息
        """
        return self._commandPost(
            "setEssence",
            {
                "target": messageId
            }
        )

    def groupConfig_get(self, group_id: int) -> dict:
        """
        获取群设置
        """
        return self._commandPost(
            "groupConfig",
            {
                "target": group_id
            },
            "get"
        )

    def groupConfig_update(self, group_id: int, config: dict) -> dict:
        """
        修改群设置
        config:
            "name":"",                  // 群名称
            "announcement":"",          // 群公告
            "confessTalk":False,        // 是否开启坦白说
            "allowMemberInvite":False,  // 是否允许群员邀请
            "autoApprove":False,        // 是否开启自动审批入群
            "anonymousChat":False       // 是否允许匿名聊天
        """
        return self._commandPost(
            "groupConfig",
            {
                "target": group_id,
                "config": config
            },
            "update"
        )

    def memberInfo_get(self, group_id: int, user_id: int) -> dict:
        """
        获取群员设置
        """
        return self._commandPost(
            "memberInfo",
            {
                "target": group_id,
                "memberId": user_id
            },
            "get"
        )

    def memberInfo_update(self, group_id: int, user_id: int, info: dict) -> dict:
        """
        修改群员设置
        info:
            "name": "群名片",
            "specialTitle": "群头衔"
        """
        return self._commandPost(
            "memberInfo",
            {
                "target": group_id,
                "memberId": user_id,
                "info": info
            },
            "update"
        )

    def memberAdmin(self, group_id: int, user_id: int, isAdmin: bool) -> dict:
        """
        修改群员管理员
        """
        return self._commandPost(
            "memberAdmin",
            {
                "target": group_id,
                "memberId": user_id,
                "assign": isAdmin
            }
        )

    def resp_newFriendRequestEvent(self, event_id: int, bot_id: int, group_id: int, operate: int, msg: str) -> dict:
        """
        使用此方法处理添加好友申请
        groupId对应申请人的群号，可能为0

        | operate | 说明                                               |
        | ------- | -------------------------------------------------- |
        | 0       | 同意添加好友                                       |
        | 1       | 拒绝添加好友                                       |
        | 2       | 拒绝添加好友并添加黑名单，不再接收该用户的好友申请 |
        """
        return self._commandPost(
            "resp/newFriendRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )

    def resp_memberJoinRequestEvent(self, event_id: int, bot_id: int, group_id: int, operate: int, msg: str) -> dict:
        """
        使用此方法处理用户入群申请

        | operate | 说明                                           |
        | ------- | ---------------------------------------------- |
        | 0       | 同意入群                                       |
        | 1       | 拒绝入群                                       |
        | 2       | 忽略请求                                       |
        | 3       | 拒绝入群并添加黑名单，不再接收该用户的入群申请 |
        | 4       | 忽略入群并添加黑名单，不再接收该用户的入群申请 |
        """
        return self._commandPost(
            "resp/memberJoinRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )

    def resp_botInvitedJoinGroupRequestEvent(self, event_id: int, bot_id: int, group_id: int, operate: int, msg: str) -> dict:
        """
        使用此方法处理Bot被邀请入群申请

        | operate | 说明     |
        | ------- | -------- |
        | 0       | 同意邀请 |
        | 1       | 拒绝邀请 |
        """
        return self._commandPost(
            "resp/botInvitedJoinGroupRequestEvent",
            {
                "eventId": event_id,
                "fromId": bot_id,
                "groupId": group_id,
                "operate": operate,
                "message": msg
            }
        )
