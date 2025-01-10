import graphs


def main() -> None:
    userInput: str = input("User: ")
    graphs.runCompiledStateGraph(graphs.graph, {"configurable": {"thread_id": "1"}}, userInput)
    pass


if __name__ == '__main__':
    main()
