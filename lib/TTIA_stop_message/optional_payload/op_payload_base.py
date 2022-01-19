from abc import ABC

from ..message_base import MessageBase


class OpPayloadBase(MessageBase, ABC):
    message_id = None

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)
