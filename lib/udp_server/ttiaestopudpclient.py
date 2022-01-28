from .clientsidehandler import ClientSideHandler
from lib import TTIABusStopMessage
from lib import EStop



class TTIAEStopUdpClient(ClientSideHandler):
    def __init__(self, host, port, estop: EStop, server_host, server_port):
        self.estop = estop
        self.server_addr = (server_host, server_port)
        super().__init__(host, port)

    def send_registration(self, msg_obj: TTIABusStopMessage):
        msg = TTIABusStopMessage(0, 'default')
        msg.header.StopID = self.estop.StopID
        msg.payload.IMSI = self.estop.IMSI
        msg.payload.IMEI = self.estop.IMEI
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)
