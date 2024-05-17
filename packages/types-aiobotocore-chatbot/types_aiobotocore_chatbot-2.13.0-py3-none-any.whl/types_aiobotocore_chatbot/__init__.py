"""
Main interface for chatbot service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chatbot import (
        ChatbotClient,
        Client,
    )

    session = get_session()
    async with session.create_client("chatbot") as client:
        client: ChatbotClient
        ...

    ```
"""

from .client import ChatbotClient

Client = ChatbotClient

__all__ = ("ChatbotClient", "Client")
