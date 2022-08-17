import collections
import struct
import sys

class Firmware:
    def __init__(self, f):
        self.infile = open(f, "r")
        self.base = 0
        self.linenum = 0

    def data(self):
        self.linenum += 1

        for line in self.infile:
            if len(line) == 0:
                break

            if line[0].strip() != ':':
                raise Exception("Wrong fileformat")

#            print (line)
            line = line[1:].strip('\r\n')
            if len(line) % 2 == 1:
                raise Exception("Wrong line len")

            # convert line to binary format
            l = []
            for i in range(0, len(line), 2):
                l.append(int(line[0+i:2+i],16))

            # check checksum
            checksum = l.pop()
            cchecksum = (0xff - (sum(l)%0x100) +1) % 0x100
            if cchecksum != checksum:
                raise Exception("Wrong checkum %02x != %02x line = %d" % (cchecksum, checksum, linenum))

            reclen = l.pop(0)
            recaddr = l.pop(0) << 8 | l.pop(0)
            rectype = l.pop(0)
#            print(reclen, recaddr, rectype)

            if reclen != len(l):
                raise Exception("Wrong data len")

            if rectype == 0x00:
                # data record
                addr = self.base + recaddr

                yield addr, bytearray(l)
            elif rectype == 0x04:
                # extended linear base addr
                self.base = 0
                for i in l:
                    self.base = self.base << 8 | l[1]
            elif rectype == 0x01:
                # end
                break


if __name__ == "__main__": 
    fw = Firmware("adf4xxx_usb_fw_2_0.hex")

    for a,d in fw.data():
        print("%x" % a, d)
