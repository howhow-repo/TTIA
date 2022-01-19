import struct
from .payload_base import PayloadBase


def fwversion_str_to_int_list(fw_str: str) -> list:
    """
    :param fw_str:
        "<num like str>.<num like str><num like str>"
        ex: "5.03", "4.89"...
    :return:
        [int, int, int]
        ex: [5, 0, 3], [4, 8, 9]...
    """
    fv = [w for w in fw_str.split('.')]
    fv1 = int(fv[0])
    fv23 = [int(w) for w in fv[1]]
    return [fv1, fv23[0], fv23[1]]


class RegUplink(PayloadBase):
    message_id = 0x00

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<15s15sBBBB', pdu)
        self.IMSI = payload[0].decode('utf-8').rstrip('\0')
        self.IMEI = payload[1].decode('utf-8').rstrip('\0')
        self.FirmwareVersion = str(payload[2]) + '.' + str(payload[3]) + str(payload[4])
        self.Reserved = payload[5]

    def to_pdu(self):
        fv1, fv2, fv3 = fwversion_str_to_int_list(self.FirmwareVersion)
        IMSI = bytearray(self.IMSI.encode('ascii'))
        IMEI = bytearray(self.IMEI.encode('ascii'))
        return struct.pack('<15s15sBBBB', IMSI, IMEI, fv1, fv2, fv3, self.Reserved)

    def from_dict(self, json):
        self.IMSI = json['IMSI']
        self.IMEI = json['IMEI']
        self.FirmwareVersion = json['FirmwareVersion']
        self.Reserved = json['Reserved']

    def to_dict(self):
        r = {
            'IMSI': self.IMSI,
            'IMEI': self.IMEI,
            'FirmwareVersion': self.FirmwareVersion,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        self.IMSI = ''
        self.IMEI = ''
        self.FirmwareVersion = '1.00'
        self.Reserved = 0
