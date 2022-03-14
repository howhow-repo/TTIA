from .EventContent import *
from ..message_base import MessageBase


class EventCode:
    Normal = 0x0000
    StopEnterLeave = 0x0001  # 進出站(圓形偵測)
    SpeedRpmOverLimitation = 0x0002  # 超轉超速(瞬轉or瞬時超速)
    SpeedUpDownSuddenly = 0x0004  # 加減速超過容許值
    DoorOpenOnDriving = 0x0008  # 行駛中車門開啟
    CarAbnormal = 0x0010  # 車輛異常
    CarStateChange = 0x0020  # 車輛狀態
    DutyOnNotSchedule = 0x0040  # 異常發車
    DriverResponse = 0x0080  # 司機回覆
    AreaLimitationEnter = 0x0100  # 進入特定區域
    TurnSharp = 0x2000  # 急轉
    TurnOver = 0x4000  # 翻車
    RouteDisallow = 0x8000  # 路線外營運

    @classmethod
    def get_default_content(cls, event_code) -> MessageBase:
        if event_code == cls.Normal:
            pass
        elif event_code == cls.StopEnterLeave:
            return StopEnterLeave({}, 'default')
        elif event_code == cls.SpeedRpmOverLimitation:
            return SpeedRpmOverLimitation({}, 'default')
        elif event_code == cls.SpeedUpDownSuddenly:
            return SpeedUpDownSuddenly({}, 'default')
        elif event_code == cls.DoorOpenOnDriving:
            return DoorOpenOnDriving({}, 'default')
        elif event_code == cls.CarAbnormal:
            return CarAbnormal({}, 'default')
        elif event_code == cls.CarStateChange:
            return CarStateChange({}, 'default')
        elif event_code == cls.DutyOnNotSchedule:
            return DutyOnNotSchedule({}, 'default')
        elif event_code == cls.DriverResponse:
            return DriverResponse({}, 'default')
        elif event_code == cls.AreaLimitationEnter:
            return AreaLimitationEnter({}, 'default')
        elif event_code == cls.TurnSharp:
            return TurnSharp({}, 'default')
        elif event_code == cls.TurnOver:
            return TurnOver({}, 'default')
        elif event_code == cls.RouteDisallow:
            return RouteDisallow({}, 'default')
