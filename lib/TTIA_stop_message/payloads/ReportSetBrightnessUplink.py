import struct
from .payload_base import PayloadBase


class ReportSetBrightnessUplink(PayloadBase):
    message_id = 0x0E
