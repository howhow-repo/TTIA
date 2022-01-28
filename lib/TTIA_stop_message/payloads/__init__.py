from .payload_base import PayloadBase

from .RegUplink import RegUplink  # 0x00
from .RegDownlink import RegDownlink  # 0x01
from .ReportBaseMsgTagUplink import ReportBaseMsgTagUplink  # 0x02

from .ReportMsgcountUplink import ReportMsgcountUplink  # 0x03
from .ReportMsgcountDownlink import ReportMsgcountDownlink  # 0x04

from .ReportUpdateMsgTagDownlink import ReportUpdateMsgTagDownlink  # 0x05
from .ReportUpdateMsgTagUplink import ReportUpdateMsgTagUplink  # 0x06

from .ReportUpdateBusinfoDownlink import ReportUpdateBusinfoDownlink  # 0x07
from .ReportUpdateBusinfoUplink import ReportUpdateBusinfoUplink  # 0x08

from .ReportAbnormalUplink import ReportAbnormalUplink  # 0x09
from .ReportAbnormalDownlink import ReportAbnormalDownlink  # 0x0A

from .ReportUpdateRouteinfoDownlink import ReportUpdateRouteinfoDownlink  # 0x0B
from .ReportUpdateRouteinfoUplink import ReportUpdateRouteinfoUplink  # 0x0C

from .ReportSetBrightnessDownlink import ReportSetBrightnessDownlink  # 0x0D
from .ReportSetBrightnessUplink import ReportSetBrightnessUplink  # 0x0E

from .ReportRebootDownlink import ReportRebootDownlink   # 0x10
from .ReportRebootUplink import ReportRebootUplink  # 0x11

from .ReportUpdateGifDownlink import ReportUpdateGifDownlink  # 0x12
from .ReportUpdateGifUplink import ReportUpdateGifUplink  # 0x13
