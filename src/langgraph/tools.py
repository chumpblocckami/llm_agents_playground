import requests
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def detect_card_name(query: str) -> str:
    """
    Given a user query, extract the name of the Magic: the Gathering card
    :return:
    """

    llm = ChatOpenAI(model="gpt-4")
    card_name = [
        SystemMessage(content=f"You extract the Magic: the Gathering card name from a given user query."),
        HumanMessage(content=query)
    ]
    attribute = [
        SystemMessage(
            content=f"You extract the attribute to extract from the query. An attribute might be: price, ability, text, power, etc..."),
        HumanMessage(content=query)
    ]
    return llm.invoke(card_name).content, llm.invoke(attribute).content


@tool
def card_data(card_name: str, attribute: str) -> str:
    """
    Provides the information for a given Magic: the Gathering card.
    Uses the Scryfall to retrieve information.
    """
    cards = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}").json()
    llm = ChatOpenAI(model="gpt-4")
    card_attribute = [
        SystemMessage(
            content=f"Associate ATTRIBUTE to the best matching word from a list of KEYS. Return the selected word from KEYS."),
        HumanMessage(content=f"ATTRIBUTE: {attribute} KEYS: {cards.keys()} ")
    ]
    attribute = llm.invoke(card_attribute).content.replace("'", "")
    return cards[attribute]


tools = [detect_card_name, card_data]
