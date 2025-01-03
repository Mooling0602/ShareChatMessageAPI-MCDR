# ShareChatMessageAPI-MCDR
Sync chat messages within different platforms.

For English users, please use translate tools at present as this project is still developing and i18n hasn't started yet.

## 介绍
本项目旨在推动各消息互通插件之间的合作，并开发一个在MCDReforged平台上统一的游戏外聊天消息派发平台和通用的解析接口。

## 依赖
Python和MCDReforged。

## API文档
### 上游，调用API
> 即负责从外部聊天平台接受收消息的插件。
- 用法：
```python
# 不清楚或者不想公开的内容，可以设置为None
message.content = "text_str_or_other"
message.type = "text" # or "data", etc.
sender_info.id = "12345678" # str, QQ number, etc.
sender_info.name = "Creeper" # str, nickname
room_info.id = "10023456" # str, QQ group number, etc.
room_info.name = "MCGroup" # str, QQ group name, etc.
platform: str = "YourPlatform"
event_dispatcher(UniversalMessageEvent, message, sender_info, room_info, platform)
```
- 导入方式：
```
from scm_api.bases import *
```
- 声明依赖
```mcdreforged.plugin.part.json
{
  ...
  "dependencies": {
    "mcdreforged": ">=2.1.0",
    "scm_api": ">=0.0.1"
  },
  ...
}
```
### 下游，监听消息事件
> 即需要接收外部聊天平台消息并进行响应的扩展性子插件，或需要获取来自其他平台的消息的消息互通插件。
>
> 若不需要派发自己的消息事件，无需声明依赖，否则请参考上一部分。
- 监听方法
```python
from mcdreforged.api.all import *

def on_load(server: PluginServerInterface, prev_module):
    pass
    server.register_event_listener('UniversalChatMessage', on_chat_message)
    pass

def on_chat_message(server, message, sender_info, room_info, platform):
    # 请根据实际情况进行处理，你可能需要进一步处理`message.content`
    formatted_message = f"[{platform}] [{room_info.name}] <{sender_info.name}> {message.content}"
    pass # 进行转发到MC等下一步操作
```

## 规范设计

### 关于消息派发

派发的消息事件应包括至少四个参数：
> 目前只能派发字符串数据，后续视情况放开其他类型的兼容。

#### `message`
> 聊天消息的主要内容，包括文本内容和媒体类型等，有两个属性值
- `content` 应为字符串，聊天的文本消息内容或未处理的原始数据
- `type` 应为字符串，表示该条消息的媒体类型

#### `sender_info` 
> 发送消息的用户的信息，有两个属性值
- `id` 应为字符串，QQ号码或者Matrix用户的user_id等，通常用于身份识别
- `name` 必须为字符串，QQ用户或者Matrix用户的显示名称/昵称等，方便辨识

#### `room_info`
> 聊天消息来自的QQ群聊或Matrix聊天室的信息等，有两个属性值
- `id` 应为字符串，QQ群号码或者Matrix聊天室的room_id等，通常用于消息源定位
- `name` 必须为字符串，QQ群或者Matrix聊天室的显示名称等，方便辨识

#### `platform` 
> 必须为字符串，声明消息所属的平台名称

### 关于聊天平台插件开发
开发者应避免直接向游戏内执行命令，或直接使用MCDR内部接口在获取到聊天消息的时候就立即转发，而应该先派发自己的消息到聊天消息事件中（在未来，使用本仓库开发的插件提供的API），然后监听聊天消息事件后，使用MCDR的`ServerInterface.psi().say(str_message)`或其他更高级的接口将消息转发到Minecraft服务器中去。

也可以边派发消息事件边转发，但不推荐。（这也会导致上面提到的建立统一分发平台的想法几乎不可能解决消息重复问题。）

另外，开发者应避免直接通过直接执行游戏指令的方式转发消息，使用MCDR的接口会更加稳定可靠，且MCDR提供的文本组件非常丰富可以满足各种需要。


## 其他
有待补充，欢迎于Issues提出意见！
