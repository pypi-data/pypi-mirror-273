# 用于messageChain的快速生成

class MessageChain(object):
    def __init__(self) -> None:
        self._data = []

    def clear(self):
        self._data = []
        return self

    def delete(self):
        del self._data[-1]
        return self

    @staticmethod
    def clean(data:dict):
        del_keys = []
        for key,value in data.items():
            if value == None:
                del_keys.append(key)
        for key in del_keys: del data[key]
        return data
                    
    def get(self) -> list:
        return self._data

    def source(self, mid: int, time: int):
        self._data.append(self.clean({
            "type": "Source",
            "id": mid,
            "time": time
        }))
        return self

    def quote(self, mid: int, groupId: int, senderId: int, targetId: int, origin: list):
        self._data.append(self.clean({
            "type": "Quote",
            "id": mid,
            "groupId": groupId,
            "senderId": senderId,
            "targetId": targetId,
            "origin": origin
        }))
        return self

    def at(self, target: int, display: str = "@Mirai"):
        self._data.append(self.clean({
            "type": "At",
            "target": target,
            "display": display
        }))
        return self

    def atAll(self):
        self._data.append(self.clean({
            "type": "AtAll"
        }))
        return self

    def face(self, faceId: int, name: str = None):
        self._data.append(self.clean({
            "type": "Face",
            "faceId": faceId,
            "name": name
        }))
        return self

    def plain(self, text: str):
        self._data.append(self.clean({
            "type": "Plain",
            "text": text
        }))
        return self

    def image(self, imageId: str = None, url: str = None, path: str = None, base64: str = None):
        self._data.append(self.clean({
            "type": "Image",
            "imageId": imageId,
            "url": url,
            "path": path,
            "base64": base64
        }))
        return self

    def flashImage(self, imageId: str = None, url: str = None, path: str = None, base64: str = None):
        self._data.append(self.clean({
            "type": "FlashImage",
            "imageId": imageId,
            "url": url,
            "path": path,
            "base64": base64
        }))
        return self

    def voice(self, voiceId: str = None, url: str = None, path: str = None, base64: str = None, length: int = None):
        self._data.append(self.clean({
            "type": "Voice",
            "voiceId": voiceId,
            "url": url,
            "path": path,
            "base64": base64,
            "length": length,
        }))
        return self

    def xml(self, txml: str):
        self._data.append(self.clean({
            "type": "Xml",
            "xml": txml
        }))
        return self

    def json(self, tjson: str):
        self._data.append(self.clean({
            "type": "Json",
            "xml": tjson
        }))
        return self

    def app(self, content: str):
        self._data.append(self.clean({
            "type": "App",
            "content": content
        }))
        return self

    def poke(self, name: str):
        self._data.append(self.clean({
            "type": "Poke",
            "name": name
        }))
        return self

    def dice(self, value: int):
        self._data.append(self.clean({
            "type": "Dice",
            "value": value
        }))
        return self

    def musicShare(self, kind: str, title: str, summary: str, jumpUrl: str, pictureUrl: str, musicUrl: str, brief: str):
        self._data.append(self.clean({
            "type": "MusicShare",
            "kind": kind,
            "title": title,
            "summary": summary,
            "jumpUrl": jumpUrl,
            "pictureUrl": pictureUrl,
            "musicUrl": musicUrl,
            "brief": brief
        }))
        return self

    def forwardMessage(self, senderId: int, mtime: int, senderName: str, messageChain: list = [], messageId: int = None):
        self._data.append(self.clean({
            "type": "Forward",
            "nodeList": [
                {
                    "senderId": senderId,
                    "time": mtime,
                    "senderName": senderName,
                    "messageChain": messageChain,
                    "messageId": messageId
                }
            ]
        }))
        return self

    def file(self, fid: int, name: str, size: int):
        self._data.append(self.clean({
            "type": "File",
            "id": fid,
            "name": name,
            "size": size
        }))
        return self
