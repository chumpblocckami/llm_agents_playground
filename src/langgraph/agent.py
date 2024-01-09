from dotenv import load_dotenv
from langchain_core.agents import AgentFinish
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import END, Graph

from src.langgraph.llm import agent_runnable
from src.langgraph.tools import tools

load_dotenv()
# Define the agent
agent = RunnablePassthrough.assign(
    agent_outcome=agent_runnable
)


# Define the function to execute tools
def execute_tools(data):
    agent_action = data.pop('agent_outcome')
    tool_to_use = {t.name: t for t in tools}[agent_action.tool]
    observation = tool_to_use.invoke(agent_action.tool_input)
    data['intermediate_steps'].append((agent_action, observation))
    return data


# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    if isinstance(data['agent_outcome'], AgentFinish):
        return "exit"
    else:
        return "continue"


workflow = Graph()

workflow.add_node("agent", agent)
workflow.add_node("tools", execute_tools)

# Set the entrypoint as `agent`
workflow.set_entry_point("agent")

# Add the edges of our agent graph
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "exit": END
    }
)
workflow.add_edge('tools', 'agent')

# Compile the graph into a LangChain Runnable
chain = workflow.compile()

if __name__ == "__main__":
    while True:
        query = input("Ask anything about Magic:the Gathering cards! ")  # "What is the price of Delver of Secrets?"
        result = chain.invoke({"input": query, "intermediate_steps": []})
        output = result['agent_outcome'].return_values["output"]
        print(output)
