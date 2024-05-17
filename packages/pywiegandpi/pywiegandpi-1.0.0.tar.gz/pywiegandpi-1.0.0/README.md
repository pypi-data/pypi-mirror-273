# pywiegandpi
Read Wiegand data from Raspberry Pi GPIO pins with a simple callback structure and automatic decoding.

## Getting Started
Install pigpio if it's not already installed:
```bash
sudo apt install pigpio
```
Enable the pigpio daemon:
```bash
sudo systemctl enable pigpiod
```

Install the required python packages by running the following command:
```bash
pip3 install -r requirements.txt
```

Use it like so:
```python
from pywiegandpi import WiegandDecoder

data_0_pin = 6
data_1_pin = 5


def callback(value):
    print("Got Wiegand data: {}".format(value))


wiegand_reader = WiegandDecoder(data_0_pin, data_1_pin, callback)

while True:
    # do something else
    pass

```

## Acknowledgements
This library is based on the original example from [joan2937](https://github.com/joan2937/pigpio/tree/master/EXAMPLES/Python/WIEGAND_CODE).
