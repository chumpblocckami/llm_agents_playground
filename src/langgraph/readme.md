# Langgraph

[Source](https://github.com/langchain-ai/langgraph)

Langgraph is a library for building stateful applications using LLMs.
It lets you coordinate multiple chains across multiple steps in cyclic manner, heavily inspired by NetworkX.

Agent and tools are seen as node of the Graphs, and they can be linked by edges.

In my opinion this architecture is very powerful for both controlling the agents flux, which tools each agent can
access and access node cycling-ly. 