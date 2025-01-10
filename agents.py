import re

from langchain_core.messages import SystemMessage, BaseMessage, HumanMessage
from langgraph.constants import END
from langgraph.types import Command

import llms
import states
from llms import generalLLM


def requirementSplitter(state: states.State) -> states.State:
    response: BaseMessage = llms.generalLLM.invoke([SystemMessage("""你是一个需求拆分器,你的任务是将用户输入的需求拆分为具体的操作。
输出格式：
一个字符串描述操作，相邻的两个操作之间用";"分割。
例：
输入：写一篇600字作文，并转发到微信朋友圈
输出：写一篇600字作文;打开微信;打开朋友圈;编辑朋友圈内容;发表朋友圈
注意：请严格按照输出格式返回结果，不要有任何多余信息。""")] + state["messages"])
    response.name = "requirementSplitter"
    return {"messages": [response]}


def actionListModifier(state: states.State) -> Command:
    actionsList: list[str] = re.split(r";", state["messages"][-1].content)
    print("操作列表：")
    for i in range(len(actionsList)):
        print(f"{i + 1}.{actionsList[i]}")
    userInput: str = input("请输入修改意见: ")
    response: BaseMessage = generalLLM.invoke([SystemMessage("""你是一个操作列表修改器，操作列表来源于需求拆分器，你需要根据用户的输入或操作列表检查器提供的修改意见来输出结果。
如果有修改意见，那么你需要严格执行修改意见，并返回修改后的操作列表；如果没有修改意见，你需要返回"~D_O_N_E~"。
操作列表格式：
一个字符串描述操作列表，相邻的两个操作之间用";"分割。
输出格式：
有修改意见时：一个字符串描述操作列表，相邻的两个操作之间用";"分割。
没有修改意见时："~D_O_N_E~"。
例：
1.操作列表：打开编辑器;新建文件;编写代码:print("Hello World");保存文件;运行程序
  修改意见：没有意见。
  输出：~D_O_N_E~
2.操作列表：写一篇600字作文;打开微信;选择朋友圈;编辑朋友圈内容;发表朋友圈
  修改意见：设置不允许标签为Z的人看
  输出：写一篇600字作文;打开微信;选择朋友圈;编辑朋友圈内容;设置可见列表(不允许标签为Z的人看);发表朋友圈
注意：请严格按照输出格式返回结果，不要有任何多余信息。"""), HumanMessage(content=userInput, name="user")] + state[
        "messages"])
    response.name = "actionModifier"
    if response.content == "~D_O_N_E~":
        return Command(
            goto="actionListChecker",
        )
    else:
        return Command(
            goto="actionListModifier",
            update={"messages": [response]}
        )


def actionListChecker(state: states.State) -> Command:
    response: BaseMessage = llms.generalLLM.invoke([SystemMessage("""是一个操作列表检查器，操作列表来源于需求拆分器和操作列表修改器。你的任务是根据用户的所有输入检查操作列表，符合用户要求返回"~D_O_N_E~"，不符合用户要求则返回修改意见(修改意见会被发送给操作列表自动修改器以重新修改操作列表)。
操作列表格式：
一个字符串描述操作列表，相邻的两个操作之间用";"分割。
输出格式：
符合用户要求时："~D_O_N_E~"。
不符合用户要求时：返回修改意见。
注意：请严格按照输出格式返回结果，不要有任何多余信息。""")] + state["messages"])
    response.name = "actionListChecker"
    if response.content == "~D_O_N_E~":
        return Command(
            goto=END
        )
    else:
        return Command(
            goto="actionListAutoModifier",
            update={"messages": [response]}
        )


def actionListAutoModifier(state: states.State) -> Command:
    response: BaseMessage = llms.generalLLM.invoke([SystemMessage("""你是一个操作列表自动修改器，操作列表来源于操作列表检查器，你需要根据操作列表检查器提供的修改意见来输出结果。你需要严格执行修改意见，并返回修改后的操作列表。
操作列表格式：
一个字符串描述操作列表，相邻的两个操作之间用";"分割。
输出格式：
一个字符串描述操作列表，相邻的两个操作之间用";"分割。
例：
操作列表：写一篇600字作文;打开微信;选择朋友圈;编辑朋友圈内容;发表朋友圈
修改意见：设置不允许标签为Z的人看
输出：写一篇600字作文;打开微信;选择朋友圈;编辑朋友圈内容;设置可见列表(不允许标签为Z的人看);发表朋友圈
注意：请严格按照输出格式返回结果，不要有任何多余信息。。""")] + state["messages"])
    response.name = "actionListAutoModifier"
    return Command(
        goto="actionListChecker",
        update={"messages": [response]}
    )


def supervisor(state: states.State) -> Command:
    # llms.generalLLM.invoke("You are a useful assistant.", state["messages"])
    return Command(
        goto=END,
    )
