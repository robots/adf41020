
import usb.core
import struct
from fw import Firmware
import time

VID = 0x0456
PID1 = 0xB40D
PID2 = 0xB403


class Fx2:

    def __init__(self):

        self.dev, fw, _ = self._find_dev()

        if self.dev.product == 'ADF4xxx USB Adapter Board':
            print("fx2: found initialized")
            #already initialized
            return

        print("fx2: uploading firmware")
        self._reset_cpu(1)
        self._upload_fw(fw)
        self._reset_cpu(0)

        time.sleep(3)

        print("fx2: looking for fx2")
        self.dev, fw, _ = self._find_dev()

        if self.dev.product == 'ADF4xxx USB Adapter Board':
            print("fx2: found initialized")
            return

        raise Exception("fx2: init failed")

    def _find_dev(self):
        model = 1
        fw = "adf4xxx_usb_fw_1_0.hex"
        dev = usb.core.find(idVendor=VID, idProduct=PID1)
        if dev is None:
            model = 2
            fw = "adf4xxx_usb_fw_2_0.hex"
            dev = usb.core.find(idVendor=VID, idProduct=PID2)
            if dev is None:
                raise Exception("no such dev")
        return dev, fw, model

    def _reset_cpu(self, on):
        ba = bytearray([0])
        
        if on:
            ba[0] = 1

        self.dev.ctrl_transfer(0x40, 0xA0, 0xE600, 0x0000, ba)

    def _upload_fw(self, fwfile):
        fw = Firmware(fwfile)
        
        for addr, data in fw.data():
            assert self.dev.ctrl_transfer(0x40, 0xA0, addr, 0x0000, data) == len(data)

    def write_adf(self, word):
        out = struct.pack("IB", word, 32)

        ret = self.dev.ctrl_transfer(0x40, 0xDD, 0x00, 0x00, out)
        if ret != len(out):
            raise Exception("transfer problem")

class FakeFx:
    def write_adf(self, word):
        print("write 0x%08x" % word)

