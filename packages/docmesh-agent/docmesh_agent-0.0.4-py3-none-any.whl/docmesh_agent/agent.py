import os

from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from docmesh_agent.toolkit import EntityToolkit, PaperToolkit, RecommendToolkit


def execute_docmesh_agent(entity_name: str, query: str, session_id: str) -> str:
    # setup react prompt
    prompt = hub.pull(os.getenv("DOCMESH_AGENT_PROMPT"))
    # setup llm
    llm = ChatOpenAI(
        base_url=os.getenv("OPENAI_CHAT_API_BASE"),
        api_key=os.getenv("OPENAI_CHAT_API_KEY"),
        model=os.getenv("OPENAI_CHAT_MODEL"),
    )
    # set up all tools
    tools = [
        *EntityToolkit(entity_name=entity_name).get_tools(),
        *PaperToolkit(entity_name=entity_name).get_tools(),
        *RecommendToolkit(entity_name=entity_name).get_tools(),
    ]
    # setup ReAct agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    # setup agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    # setup memory database
    memory_store = os.getenv("MYSQL_URL")
    # bind agent and memory
    agent_with_memory = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id,
            connection_string=memory_store,
        ),
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    # run the agent!
    result = agent_with_memory.invoke(
        {"input": query},
        config={"configurable": {"session_id": session_id}},
    )
    # retrieve output
    output = result["output"]

    return output
