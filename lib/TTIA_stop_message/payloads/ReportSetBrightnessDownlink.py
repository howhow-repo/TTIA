import struct
from .payload_base import PayloadBase


class ReportSetBrightnessDownlink(PayloadBase):
    message_id = 0x0D
