"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class controlEstimateState(object):
    __slots__ = ["states", "timestamp"]

    __typenames__ = ["double", "int64_t"]

    __dimensions__ = [[5], None]

    def __init__(self):
        self.states = [ 0.0 for dim0 in range(5) ]
        self.timestamp = 0

    def encode(self):
        buf = BytesIO()
        buf.write(controlEstimateState._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack('>5d', *self.states[:5]))
        buf.write(struct.pack(">q", self.timestamp))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != controlEstimateState._get_packed_fingerprint():
            raise ValueError("Decode error")
        return controlEstimateState._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = controlEstimateState()
        self.states = struct.unpack('>5d', buf.read(40))
        self.timestamp = struct.unpack(">q", buf.read(8))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if controlEstimateState in parents: return 0
        tmphash = (0x20c3f2977cdd6e55) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if controlEstimateState._packed_fingerprint is None:
            controlEstimateState._packed_fingerprint = struct.pack(">Q", controlEstimateState._get_hash_recursive([]))
        return controlEstimateState._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

