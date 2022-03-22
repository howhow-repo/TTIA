import unittest
from lib import TTIABusStopMessage


class TestStopMsgBaseCase(unittest.TestCase):
    """
        Base type for testing TTIA python obj.
        Please write test case here with method name start with "test",
        such as "test_bla_bla_bla...."
    """
    pdu_pack = None
    MESSAGEID = None

    def test_from_to_pdu_by_raw_pdu(self):
        """
            raw_pdu --init--> py_obj --to_pdu-> created_pdu (create by py_obj)

            created_pdu should be same as raw_pdu.
        """
        assert self.pdu_pack is not None and self.MESSAGEID is not None, \
            "'pdu_pack' and 'MESSAGEID' must be define for test case."

        msg = TTIABusStopMessage(init_data=self.pdu_pack, init_type='pdu')
        self.assertEqual(msg.to_pdu(), self.pdu_pack)

    def test_from_to_dict_by_default_creation(self):
        """
            --init by default--> py_obj --to_dict-> obj_dict (create by py_obj)
            obj_dict --init--> new_py_obj --to_dict-> new_obj_dict

            obj_dict should be same as new_obj_dict.
        """
        assert self.pdu_pack is not None and self.MESSAGEID is not None, \
            "'pdu_pack' and 'MESSAGEID' must be define for test case."

        default_msg = TTIABusStopMessage(init_data=self.MESSAGEID, init_type='default')
        obj_dict = default_msg.to_dict()
        from_dict_msg = TTIABusStopMessage(init_data=obj_dict, init_type='dict')
        self.assertEqual(from_dict_msg.to_dict(), obj_dict)

    def test_from_to_pdu_by_default_creation(self):
        """
            --init by default--> py_obj --to_pdu-> created_pdu (create by py_obj)
            created_pdu --init--> new_py_obj

            py_obj.to_pdu() should be same as new_py_obj.to_pdu()
            py_obj.to_dict() should be same as new_py_obj.to_dict()
        """
        assert self.pdu_pack is not None and self.MESSAGEID is not None, \
            "'pdu_pack' and 'MESSAGEID' must be define for test case."

        default_msg = TTIABusStopMessage(init_data=self.MESSAGEID, init_type='default')
        msg = TTIABusStopMessage(init_data=default_msg.to_pdu(), init_type='pdu')
        self.assertEqual(msg.to_pdu(), default_msg.to_pdu())
        self.assertEqual(msg.to_dict(), default_msg.to_dict())
