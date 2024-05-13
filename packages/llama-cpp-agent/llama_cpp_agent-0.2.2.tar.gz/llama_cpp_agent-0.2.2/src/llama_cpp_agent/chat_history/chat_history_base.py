import json
from abc import abstractmethod, ABC
from enum import Enum
from typing import List, Dict

from llama_cpp_agent.chat_history.messages import ChatMessage


class ChatHistory(ABC):
    @abstractmethod
    def get_chat_messages(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def add_message(self, message: Dict[str, str]):
        pass

    @abstractmethod
    def get_messages_count(self):
        pass

    @abstractmethod
    def edit_message(self, index: int, edited_message: Dict[str, str]):
        pass

    @abstractmethod
    def get_message(self, index) -> Dict[str, str]:
        pass


class ChatMessageStore(ABC):

    @abstractmethod
    def get_messages_count(self):
        pass

    @abstractmethod
    def add_message(self, message: ChatMessage):
        pass

    @abstractmethod
    def edit_message(self, index: int, edited_message: ChatMessage):
        pass

    @abstractmethod
    def add_user_message(self, message: str):
        pass

    @abstractmethod
    def add_assistant_message(self, message: str):
        pass

    @abstractmethod
    def add_system_message(self, message: str):
        pass

    @abstractmethod
    def remove_last_message(self):
        pass

    @abstractmethod
    def remove_last_k_messages(self, k: int):
        pass

    @abstractmethod
    def get_message(self, index: int) -> ChatMessage:
        pass

    @abstractmethod
    def get_last_message(self) -> ChatMessage:
        pass

    @abstractmethod
    def get_last_k_messages(self, k: int) -> List[ChatMessage]:
        pass

    @abstractmethod
    def get_messages(self, k: int) -> List[ChatMessage]:
        pass

    @abstractmethod
    def get_all_messages(self) -> List[ChatMessage]:
        pass
