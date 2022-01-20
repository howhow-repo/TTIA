import unittest
from lib import TTIABusStopMessage


class TestBaseCase(unittest.TestCase):
    pdu_pack = None
    MESSAGEID = None

    def test_from_to_pdu_by_raw_pdu(self):
        assert self.pdu_pack is not None and self.MESSAGEID is not None, \
            "'pdu_pack' and 'MESSAGEID' must be define for test case."

        msg = TTIABusStopMessage(init_data=self.pdu_pack, init_type='pdu')
        self.assertEqual(msg.to_pdu(), self.pdu_pack)

    def test_from_to_dict_by_default_creation(self):
        assert self.pdu_pack is not None and self.MESSAGEID is not None, \
            "'pdu_pack' and 'MESSAGEID' must be define for test case."

        default_msg = TTIABusStopMessage(init_data=self.MESSAGEID, init_type='default')
        obj_dict = default_msg.to_dict()
        from_dict_msg = TTIABusStopMessage(init_data=obj_dict, init_type='dict')
        self.assertEqual(from_dict_msg.to_dict(), obj_dict)

    def test_from_to_pdu_by_default_creation(self):
        assert self.pdu_pack is not None and self.MESSAGEID is not None, \
            "'pdu_pack' and 'MESSAGEID' must be define for test case."

        default_msg = TTIABusStopMessage(init_data=self.MESSAGEID, init_type='default')
        msg = TTIABusStopMessage(init_data=default_msg.to_pdu(), init_type='pdu')
        self.assertEqual(msg.to_pdu(), default_msg.to_pdu())
        self.assertEqual(msg.to_dict(), default_msg.to_dict())
