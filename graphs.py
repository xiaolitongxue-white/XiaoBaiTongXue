import sqlite3

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

import agents
import states
import utils

connect: sqlite3.Connection = sqlite3.connect("memory.data", check_same_thread=False)
memory: SqliteSaver = SqliteSaver(connect)

graphBuilder: StateGraph = StateGraph(states.State)
graphBuilder.add_node("requirementAnalyzer", agents.requirementAnalyzer)
graphBuilder.add_node("supervisor", agents.supervisor)
graphBuilder.set_entry_point("requirementAnalyzer")
graph: CompiledStateGraph = graphBuilder.compile(
    checkpointer=memory,
)


def runCompiledStateGraph(compiledStateGraph: CompiledStateGraph, config: RunnableConfig, userInput: str):
    for event in compiledStateGraph.stream({"messages": [{"role": "user", "content": userInput, "name": "user"}]},
                                           config=config):
        for value in event.values():
            if value is None:
                continue
            messages: list[BaseMessage] = value["messages"]
            for message in messages:
                utils.printMessage(message)
