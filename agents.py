from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.constants import END
from langgraph.types import Command

import llms
import states

def requirementAnalyzer(state: states.State) -> Command:
    message: BaseMessage = llms.generalLLM.invoke(
        [SystemMessage("You are a requirement analyzer.", name="system")] + state["messages"])
    message.name = "requirementAnalyzer"
    return Command(
        goto="supervisor",
        update={"messages": [message]}
    )


def supervisor(state: states.State) -> Command:
    # llms.generalLLM.invoke("You are a useful assistant.", state["messages"])
    return Command(
        goto=END,
    )
