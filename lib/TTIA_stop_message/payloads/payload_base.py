from abc import ABC

from ..message_base import MessageBase


class PayloadBase(MessageBase, ABC):
    message_id = None
    message_cname = None

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def self_assert(self):
        raise NotImplementedError

    def from_lazy_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys():
                self.__setattr__(item, setting_config[item])
