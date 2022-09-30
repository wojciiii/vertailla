from intelhex import IntelHex
import os

BIN_EXT = "bin"
INTEL_HEX_EXT = "hex"


def align_up(num, align):
    assert (align & (align - 1) == 0) and align != 0
    return (num + (align - 1)) & ~(align - 1)


class Image:

    def __init__(self):
        self.payload = []
        self.base_addr = 0
        self.max_addr = 0

    def load(self, path):
        """Load an image from a given file"""
        ext = os.path.splitext(path)[1][1:].lower()
        try:
            if ext == INTEL_HEX_EXT:
                ih = IntelHex(path)
                self.payload = ih.tobinarray()
                self.base_addr = ih.minaddr()
                self.max_addr = ih.maxaddr()
            else:
                with open(path, 'rb') as f:
                    self.payload = f.read()
        except FileNotFoundError as e:
            raise e

    def get_base_address(self):
        return self.base_addr

    def get_max_address(self):
        return self.max_addr

    def save(self, path):
        """Save an image from a given file"""
        ext = os.path.splitext(path)[1][1:].lower()
        if ext == INTEL_HEX_EXT:
            # input was in binary format, but HEX needs to know the base addr
            h = IntelHex()
            h.frombytes(bytes=self.payload, offset=self.base_addr)
            h.tofile(path, 'hex')
        else:
            with open(path, 'wb') as f:
                f.write(self.payload)

