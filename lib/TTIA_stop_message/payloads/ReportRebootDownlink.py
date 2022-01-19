import struct
from .payload_base import PayloadBase


class ReportRebootDownlink(PayloadBase):
    message_id = 0x10
