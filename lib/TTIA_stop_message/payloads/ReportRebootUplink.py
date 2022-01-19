import struct
from .payload_base import PayloadBase


class ReportRebootUplink(PayloadBase):
    message_id = 0x11
