from mcdreforged.api.all import *
from .bases import UniversalMessageEvent
from .config import load_config

psi = ServerInterface.psi()


def on_load(server: PluginServerInterface, prev_module):
    config = load_config(server)
    if config["enable"]["listen_only"]:
        server.register_event_listener('UniversalChatMessage', debug)
    if config["enable"]["test"]:
        server.register_command(
            Literal('!!scm_api')
            .then(
                Literal('test')
                .runs(
                    lambda src: test(src)
                )
            )
        )

# 你可以调用这个派发任意类型的事件，不仅仅是聊天消息
# 用这个方法派发的事件是非预期的，你只能在自己的插件中使用或者自行定义自己的规范
def general_event_dispatcher(event: type[PluginEvent], *args, **kwargs):
    event_instance = event(*args, **kwargs)
    psi.dispatch_event(event_instance, args)
    psi.logger.debug("Event dispatched to MCDR!")

# 这个方法是提供给所有消息互通类插件开发者的，任意下游插件可以直接监听这个事件。
def event_dispatcher(UniversalMessageEvent, *args, **kwargs):
    event_instance = UniversalMessageEvent(*args, **kwargs)
    psi.dispatch_event(event_instance, args)
    psi.logger.debug("Event dispatched to MCDR!")

def test(src: CommandSource):
    # 若不导入，则需要自行构建，可能导致消息事件中的数据不规范。
    from scm_api.bases import message, sender_info, room_info
    message.content = "这是一条测试消息"
    message.type = "text"
    sender_info.id = "12345678"
    sender_info.name = "Steve"
    room_info.id = "100023456"
    room_info.name = "Server"
    platform = "MCDReforged"
    event_dispatcher(UniversalMessageEvent, message, sender_info, room_info, platform)
    src.reply("event dispatched!")

def debug(server: PluginServerInterface, message, sender_info, room_info, platform):
    if message.type == "text":
        chat_message = f"[{platform}] [{room_info.name}] <{sender_info.name}> {message.content}"
    elif message.type == "data":
        formatted_message_content = None # 根据实际情况处理
        chat_message = f"[{platform}] [{room_info.name}] <{sender_info.name}> {formatted_message_content}"
    else:
        pass
    server.logger.info(
        f"Debug Info" + "\n" +
        f"Message - content: {message.content} - type: {message.type}" + "\n" +
        f"Sender info - id: {sender_info.id} - name: {sender_info.name}" + "\n" +
        f"Room info - id: {room_info.id} - name: {room_info.name}" + "\n" +
        f"Platform: {platform}"
    )
    # 亦可使用更简单的server.broadcast(chat_message)
    server.logger.info(chat_message)
    server.say(chat_message)
