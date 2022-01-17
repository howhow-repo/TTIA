from abc import ABC

from ..message_base import MessageBase


class PayloadBase(MessageBase, ABC):
    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)