# ShareChatMessageAPI-MCDR
Sync chat messages within different platforms.

For English users, please use translate tools at present as this project is still a plan.

## 介绍
本项目旨在推动各消息互通插件之间的合作，并开发一个在MCDReforged平台上统一的游戏外聊天消息派发和解析平台。

## 依赖
Python和MCDReforged。

## 原理
- 使用MCDReforged提供的`ServerInterface.psi().dispatch_event(...)`设计一个事件派发器，消息互通插件统一使用这个派发器在MCDReforged中派发聊天消息事件。
> 这个仓库将致力于开发一个API类型的插件，供其他开发者完成这个工作。目前可以参考 https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/matrix_sync/event/__init__.py 中的`event_dispatcher`函数。
- 消息互通插件乃至更下游的子插件使用MCDReforged提供的事件监听器（`ServerInterface.psi().register_event_listener(...)`）解析聊天消息事件，并转发自己的消息到游戏中、转发其他平台的消息到自己所支持平台的群聊、聊天室中去，实现不同平台之间和Minecraft的聊天消息共享。
> 统一的分发平台理论上是可行的，但笔者不认为做这样一个平台有什么太大意义，应该由各家插件自行完成分发，以避免发生冲突

## 规范设计

### 关于消息派发

派发的消息事件应包括至少四个参数：
- `platform` 外部的聊天平台，如QQ、Matrix、Discord、Telegram等
- `sender_info` 发送消息的用户的信息，包括名字（或昵称）`name`和用户名（或数字编号）`id`等
- `message` 聊天消息的主要内容，包括文本内容和媒体类型等
- `group_info` 聊天消息产生的群聊、聊天室的信息，包括`name`群聊名称、`id`群号等

### 关于聊天平台插件开发
开发者应避免直接向游戏内执行命令，或直接使用MCDR内部接口在获取到聊天消息的时候就立即转发，而应该先派发自己的消息到聊天消息事件中（在未来，使用本仓库开发的插件提供的API），然后监听聊天消息事件后，使用MCDR的`ServerInterface.psi().say(str_message)`或其他更高级的接口将消息转发到Minecraft服务器中去。

也可以边派发消息事件边转发，但不推荐。（这也会导致上面提到的建立统一分发平台的想法几乎不可能解决消息重复问题。）

另外，开发者应避免直接通过直接执行游戏指令的方式转发消息，使用MCDR的接口会更加稳定可靠，且MCDR提供的文本组件非常丰富可以满足各种需要。


## 其他
有待补充，欢迎于Issues提出意见！
