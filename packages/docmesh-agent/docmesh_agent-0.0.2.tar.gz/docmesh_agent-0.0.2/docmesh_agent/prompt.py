from langchain_core.prompts import PromptTemplate

# this prompt is modified from the official ReAct prompt
# but with memroy support
prompt_with_memory = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Our previous conversation:

{chat_history}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""
MEMORY_REACT_PROMPT = PromptTemplate.from_template(prompt_with_memory)
