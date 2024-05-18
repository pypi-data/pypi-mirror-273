import os

from colorama import Fore, Style
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from docmesh_agent.toolkit import CommonToolkit, EntityToolkit, PaperToolkit, RecommendToolkit


class TermColor:
    tool: str = f"{Fore.MAGENTA}{Style.DIM}"
    observation: str = f"{Fore.YELLOW}{Style.DIM}"
    output: str = f"{Fore.GREEN}{Style.BRIGHT}"
    error: str = f"{Fore.RED}{Style.BRIGHT}"
    end: str = f"{Style.RESET_ALL}"


def _setup_agent(entity_name: str) -> RunnableWithMessageHistory:
    # setup docmesh agent prompt
    prompt = hub.pull(os.getenv("DOCMESH_AGENT_PROMPT"))
    # setup llm
    llm = ChatOpenAI(
        base_url=os.getenv("OPENAI_CHAT_API_BASE"),
        api_key=os.getenv("OPENAI_CHAT_API_KEY"),
        model=os.getenv("OPENAI_CHAT_MODEL"),
    )
    # set up all tools
    tools = [
        *CommonToolkit(entity_name=entity_name).get_tools(),
        *EntityToolkit(entity_name=entity_name).get_tools(),
        *PaperToolkit(entity_name=entity_name).get_tools(),
        *RecommendToolkit(entity_name=entity_name).get_tools(),
    ]
    # build docmesh agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    # setup agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)
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

    return agent_with_memory


def execute_docmesh_agent(entity_name: str, query: str, session_id: str) -> str:
    agent_with_memory = _setup_agent(entity_name)
    # run the agent!
    try:
        result = agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )
        # retrieve output
        output = result["output"]
        msg = f"\n{TermColor.output}[✔️ answer]: \n{output}{TermColor.end}\n"
    except Exception as e:
        msg = f"\n{TermColor.error}[✘ error]: \n{e}\ndocmesh agent stopped!{TermColor.end}\n"

    return msg


async def aexecute_docmesh_agnet(entity_name: str, query: str, session_id: str) -> str:
    agent_with_memory = _setup_agent(entity_name)
    # astream the agent!
    try:
        async for chunk in agent_with_memory.astream(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        ):
            # tool using
            if "actions" in chunk:
                for action in chunk["actions"]:
                    msg = f"\n{TermColor.tool}[⚒︎ {action.tool}]: {action.tool_input}{TermColor.end}"
                    yield msg.encode()
            # observation
            elif "steps" in chunk:
                for step in chunk["steps"]:
                    # observations could be real long if encountered PDF content
                    # so we truncate all obseravations over 2000 characters
                    truncate_threshold = 2000
                    if len(step.observation) > truncate_threshold:
                        observation = f"\nbservation exceeds {truncate_threshold} characters and has been omitted...\n"
                    else:
                        observation = step.observation
                    msg = f"\n{TermColor.observation}[⌕ observation]: {observation}{TermColor.end}"
                    yield msg.encode()
            # output
            elif "output" in chunk:
                output = chunk["output"]
                msg = f"\n{TermColor.output}[✔️ answer]: \n{output}{TermColor.end}\n"
                yield msg.encode()
    except Exception as e:
        msg = f"\n{TermColor.error}[✘ error]: \n{e}\ndocmesh agent stopped!{TermColor.end}\n"
        yield msg.encode()
