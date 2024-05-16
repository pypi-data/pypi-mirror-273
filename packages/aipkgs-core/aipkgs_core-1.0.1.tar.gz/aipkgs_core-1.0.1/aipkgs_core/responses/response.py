from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Union


class ErrorResponseInterface:
    __metaclass__ = ABCMeta

    @classmethod
    def forge_dict(cls, data: dict = None, error_code: Union[int, Enum] = None, status_code: int = None): raise NotImplementedError

    @classmethod
    def forge(cls, title: str = None, message: str = None, message_code: str = None, error_code: Union[int, Enum] = None, data: dict = None, status_code: int = None): raise NotImplementedError

    @classmethod
    def forge_localized(cls, title_key: str = None, message_key: str = None, error_code: Union[int, Enum] = None, status_code: int = None): raise NotImplementedError
    # @abstractmethod
    # def make_response(cls): return "1.0"


class SuccessResponseInterface:
    __metaclass__ = ABCMeta

    @classmethod
    def forge_dict(cls, data: dict = None, status_code: int = None): raise NotImplementedError

    @classmethod
    def forge_raw(cls, status_code: int = None, **kwargs): raise NotImplementedError

    @classmethod
    def forge(cls, title: str = None, message: str = None, data: dict = None, status_code: int = None): raise NotImplementedError


class VerboseResponseInterface:
    __metaclass__ = ABCMeta

    @classmethod
    def forge(cls, data: dict = None, status_code: int = None): raise NotImplementedError
    # @abstractmethod
    # def make_response(cls): return "1.0"
