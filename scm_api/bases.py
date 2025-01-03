from mcdreforged.api.all import *

psi = ServerInterface.psi()


class message(Serializable):
    content: str # 待解析的消息内容，应为字符串
    type: str # 消息类型的可识别名称

class sender_info(Serializable):
    id: str # Matrix 用户 ID 或 QQ 号
    name: str # 用户的显示名称

class room_info(Serializable):
    id: str # Matrix 房间 ID 或 QQ 群号码
    name: str # Matrix 房间显示名称或 QQ 群名称
    
class UniversalMessageEvent(PluginEvent):
    def __init__(self, message, sender_info, room_info, platform: str):
        super().__init__('UniversalChatMessage')
        self.message = message
        self.sender_info = sender_info
        self.room_info = room_info
        # 平台名称：如 QQ、Matrix 等，可以附加上自己定制的插件名避免同平台冲突，但不能解决重复问题，只能引导用户不同时使用适用于某个平台的多个插件
        self.platform = platform
