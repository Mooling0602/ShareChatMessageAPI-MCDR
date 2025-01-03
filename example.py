from mcdreforged.api.types import PluginServerInterface


def listen_message(server: PluginServerInterface):
    server.register_event_listener("UniversalChatMessage", on_chat_message)

def on_chat_message(server, message, sender_info, room_info, platform: str):
    if message.type == "text":
        chat_message = f"[{platform}] [{room_info.name}] <{sender_info.name}> {message.content}"
    elif message.type == "data":
        formatted_message_content = None # 根据实际情况处理
        chat_message = f"[{platform}] [{room_info.name}] <{sender_info.name}> {formatted_message_content}"
    else:
        pass
    # 亦可使用更简单的server.broadcast(chat_message)
    server.logger.info(chat_message, "Message")
    server.say(chat_message)
