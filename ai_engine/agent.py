"""
LangGraph-based Travel Advisor Agent.
Orchestrates multi-step reasoning with tool calling.
"""
import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from .client import get_llm
from .prompts import build_system_prompt
from .tools import ALL_TOOLS

logger = logging.getLogger('ai_engine')


class TravelAdvisorAgent:
    """
    AI agent that handles travel advisory conversations.

    Uses LangGraph's ReAct agent pattern to:
    - Process user messages with conversation history
    - Decide when to use specialized tools
    - Return structured travel advice
    """

    def __init__(self, user_preferences: dict | None = None):
        self.llm = get_llm()
        self.system_prompt = build_system_prompt(user_preferences)
        self.agent = create_react_agent(
            model=self.llm,
            tools=ALL_TOOLS,
        )

    def chat(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
    ) -> str:
        """
        Send a message to the travel advisor and get a response.

        Args:
            user_message: The user's message text.
            conversation_history: List of prior messages as
                [{"role": "user"|"assistant", "content": "..."}]

        Returns:
            The AI assistant's response text.
        """
        # Build message list
        messages = [SystemMessage(content=self.system_prompt)]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

        # Add current message
        messages.append(HumanMessage(content=user_message))

        logger.info(f"Invoking agent with {len(messages)} messages")

        try:
            result = self.agent.invoke({"messages": messages})

            # Extract the last AI message from the result
            response_messages = result.get("messages", [])
            for msg in reversed(response_messages):
                if isinstance(msg, AIMessage) and msg.content:
                    logger.info("Agent response received successfully")
                    return msg.content

            return "I apologize, but I wasn't able to generate a response. Please try rephrasing your question."

        except Exception as e:
            logger.error(f"Agent error: {e}", exc_info=True)
            return (
                "I encountered an error while processing your request. "
                "Please try again in a moment. If the issue persists, "
                "check that the API key is configured correctly."
            )
