from langchain_core.messages import BaseMessage


def convertMessageTypeToRole(messageType: str) -> str:
    if messageType in ("human", "user"):
        return "user"
    elif messageType in ("ai", "assistant"):
        return "assistant"
    elif messageType in ("system", "developer"):
        return "system"
    elif messageType == "function":
        return "function"
    elif messageType == "tool":
        return "tool"
    else:
        raise ValueError("Invalid message type '" + messageType + "'")


def printMessage(message: BaseMessage)->None:
    match convertMessageTypeToRole(message.type):
        case "user":
            print("User(" + message.name + "): " + message.content)
        case "assistant":
            print("Assistant(" + message.name + "): " + message.content)
        case "system":
            print("System: " + message.content)
        case "function":
            print("Function(" + message.name + "): " + message.content)
        case "tool":
            print("Tool(" + message.name + "): " + message.content)
