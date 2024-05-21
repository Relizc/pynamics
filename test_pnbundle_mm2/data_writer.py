out = open("textmap.pntexture", "wb")

import random

def get_id():
    return random.randint(-2**31, 2 ** 31 - 1)

def by(x, l=4):
    return x.to_bytes(l, byteorder="little")

PROT: int = 145

def STR_HASH_UINT32(inp: str):
    hash = 0
    for ch in inp:
        hash = (hash * 0xf5fcaad4 ^ ord(ch) * 0x663e3d4e) & 0xFFFFFFFF
    return hash

out.write(b"PN")
out.write(PROT.to_bytes(2, byteorder="little")) # protocol version

# texture definitions
# how a tile is defined:
out.write(by(2, 2)) # number of frames.

# Play pointer

# Frame 1
out.write(by(STR_HASH_UINT32("MM2_POINTER"))) # tile hash (basically an id)
x, y, a, b = 146, 0, 146 + 8, 0 + 8 # Image range from (x, y) to (a, b)
out.write(by(x, 2))
out.write(by(y, 2))
out.write(by(a, 2))
out.write(by(b, 2))

# Frame 2 (Each frame is 20 bytes fingerprint + four coords)
# each frame has to be with the same fingerprint
out.write(by(STR_HASH_UINT32("MM2_POINTER"))) # tile hash (basically an id)
x, y, a, b = 146, 9, 146 + 8, 9 + 8 # Image range from (x, y) to (a, b)
out.write(by(x, 2))
out.write(by(y, 2))
out.write(by(a, 2))
out.write(by(b, 2))

out.close()
