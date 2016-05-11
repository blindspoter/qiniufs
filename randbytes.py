# -*- coding: utf-8 -*-

import os
import binascii
import time


if hasattr(os, 'urandom'):
    def randbytes(bytes):
        """Return bits of random data as a hex string."""
        return binascii.hexlify(os.urandom(bytes))
elif os.path.exists('/dev/urandom'):
    def randbytes(bytes):
        """Return bits of random data as a hex string."""
        return binascii.hexlify(open("/dev/urandom").read(bytes))
else:
    import sha

    class _PRNG:

        def __init__(self):
            self.state = sha.new(str(time.time() + time.clock()))
            self.count = 0

        def _get_bytes(self):
            self.state.update('%s %d' % (time.time() + time.clock(),
                                         self.count))
            self.count += 1
            return self.state.hexdigest()

        def randbytes(self, bytes):
            """Return bits of random data as a hex string."""
            s = ""
            chars = 2 * bytes
            while len(s) < chars:
                s += self._get_bytes()
            return s[:chars]

    randbytes = _PRNG().randbytes
