# TTIA Stop library
<hr>
A libary for encoding/decoding binary of TTIA Stop protocal.

## installation
```pip install -r requirements.txt```

## Use cases:

1. Decode coming udp binary message:
```python
from lib import TTIABusStopMessage

coming_udp_binary = b'IBST\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f' \
                    b'\x00\x00\x00\x00\xa4\xa4\xa4\xe5\xaf\xb8\xa6W\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Eng Stop\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<' \
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,\x01,\x01\x01'


msg = TTIABusStopMessage(init_data=coming_udp_binary, init_type='pdu')
print(msg.to_dict())  # you can check data by printing out .to_dict()
# >> {'header': {'ProtocolID': 'IBST', 'Protoc.....
print(msg.payload.StopCName)  # or check directly by property name
# >> 中文站名
msg.payload.StopCName = "新站名"  # or update property directly
print(msg.payload.StopCName)
# >> 新站名
```
2. Create an empty msg:
```python
from lib import TTIABusStopMessage

msg = TTIABusStopMessage(init_data=0, init_type='default')
msg.payload.IMSI, msg.payload.IMEI = 'new_IMSI', 'new_IMSI'
print(msg.payload.to_dict())
# >> {'IMSI': 'new_IMSI', 'IMEI': 'new_IMSI', 'FirmwareVersion': '1.00', 'Reserved': 0}
```

3. Create an msg with dict:
```python
from lib import TTIABusStopMessage

data_dict = {"header":{...}, "payload": {...}}
# please aware with every prop's data type
msg = TTIABusStopMessage(init_data=data_dict, init_type='dict')

```

## Auto testing
To run test, just simply run main_test.py.
it will run through test py files in lib/TTIA_stop_message/test
