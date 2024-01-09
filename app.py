import streamlit as st
from dotenv import load_dotenv

from src.langgraph.agent import chain

load_dotenv()

st.set_page_config(page_title="Scryfall chat", page_icon="👋")


@st.cache_resource(show_spinner=False)
def load_resources():
    return chain

def init():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


init()
llm = load_resources()

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.write('Chat with Scryfall!')

with col3:
    st.write(' ')

if question := st.chat_input("Write here"):
    with st.expander("Past conversation"):
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            agent_thinking = llm.invoke({"input": question, "intermediate_steps": []})
            answer = agent_thinking['agent_outcome'].return_values["output"]
        message_placeholder.markdown(answer)

    st.session_state["chat_history"].extend([{"role": "user", "content": question},
                                             {"role": "assistant", "content": answer}])
