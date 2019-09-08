
from . import dataio as d
from . import gheader as gh


###############################################################
## .zab  (ZCAB) File Start
###############################################################

class ZAB: # ZCAB:
    'Zelda Course Arrangement Binary (.zab)'
    def __init__(self, data):
        self.data = data
        self.pointer = 16
        self.readfilelength = d.UInt32(self.data, 4)
        self.elementcount = d.UInt32(self.data, 8)
        tmp = d.UInt32(self.data, 20)
        self.CABM = ZCAB_CABM(self.data[16:16+tmp])
        tmp2 = d.UInt32(self.data, 20+tmp)
        self.CABI = ZCAB_CABI( self.data[16+tmp:16+tmp+tmp2])

    def calculate_size(self):
        self.size = 16 + self.CABM.calculate_size() + self.CABI.calculate_size()
        return self.size

    def save(self):
        hs = 16
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("5a434142") # ZCAB
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt32(buffer, 8, 2) # Child Elements

        buffer[12:] = bytearray.fromhex("FFFFFFFF")

        buffer = buffer + self.CABM.save()
        buffer = buffer + self.CABI.save()

        return buffer


class ZCAB_CABM(gh.ZDS_GenericElementHeaderRaw):
    'Zelda Course Arrangement Binary (.zab) Course Arrangement Binary Maplist '
    # Course Arangement Binary Maplist
    def init(self):
        self.unknwn1 = d.UInt8(self.data, 8)
        self.unknwn2 = d.UInt8(self.data, 9)

        self.padding1 = d.UInt16(self.data, 10) # = 0x0000  |  TO BE CONFIRMED!

        if not self.padding1 == 0:
            print("Padding has NON Zero Value: "+str(self.padding1))

        self.mapsizex = d.UInt8(self.data, 12)
        self.mapsizey = d.UInt8(self.data, 13)

        self.children_count = d.UInt16(self.data, 14)
        self.pointer = 16

        self.children = []

        for i in range(self.children_count):
            self.children.append( ZCAB_CABM_CE( self.data[self.pointer:self.pointer+8], i ) )
            self.pointer = self.pointer + 8

        print("MBAC Size: "+str(self.size))
        print("MBAC UNKNW1: "+str(self.unknwn1))
        print("MBAC UNKNW2: "+str(self.unknwn2))
        # print("MBAC PAD1: "+str(self.padding1))
        print("MBAC MS_X: "+str(self.mapsizex))
        print("MBAC MS_Y: "+str(self.mapsizey))
        print("MBAC Children: "+str(self.children_count))

    def calculate_size(self):
        self.size = 16 + 8 * len(self.children)
        return self.size

    def save(self):
        hs = 16
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("4d424143") # MBAC
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt8(buffer, 8, self.unknwn1) # Unknown #1
        buffer = d.w_UInt8(buffer, 9, self.unknwn2) # Unknown #2

        buffer = d.w_UInt16(buffer, 10, self.padding1) # Padding #1

        buffer = d.w_UInt8(buffer, 12, self.mapsizex) # MapSize X
        buffer = d.w_UInt8(buffer, 13, self.mapsizey) # MapSize Y

        buffer = d.w_UInt16(buffer, 14, len(self.children)) # Children Count #1
        # buffer = d.w_UInt16(buffer, 10, 65535) # Write 0xFFFF

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

class ZCAB_CABM_CE:
    'Zelda Course Arrangement Binary (.zab) Course Arrangement Binary Maplist Child Element'
    # Course Arangement Binary Maplist CE
    def __init__(self, data, num):
        self.data = data
        self.size = len(data)
        self.uid = d.UInt8(data, 0)
        self.localid = d.UInt8(data, 1)
        self.areaid = d.UInt8(data, 2)
        self.floornum = d.Int8(data, 3)
        # TODO: Find out what the Bytes change ingame
        print("M_CE: UID:"+str(self.uid)+ " LID:"+str(self.localid)+ " AID:"+str(self.areaid)+" FNUM:"+str(self.floornum)+" HEX:"  +str(self.data[4:].hex()) + "   [:"+str(num)+"]")

    def save(self):
        buffer = self.data

        buffer = d.w_UInt8(buffer, 0, self.uid)
        buffer = d.w_UInt8(buffer, 1, self.localid)
        buffer = d.w_UInt8(buffer, 2, self.areaid)
        buffer = d.w_Int8(buffer, 3, self.floornum)

        return buffer

class ZCAB_CABI(gh.ZDS_GenericElementHeader):
    'Zelda Course Arrangement Binary (.zab) Course Arangement Binary Icons'
    def init(self):
        self.pointer = 12

        for i in range(self.children_count):
            self.children.append( ZCAB_CABI_CE( self.data[self.pointer:self.pointer+12] , i ) )
            self.pointer = self.pointer + 12

        print("IBAC Size: "+str(self.size))
        print("IBAC Children: "+str(self.children_count))

    def calculate_size(self):
        self.size = 12 + 12 * len(self.children)
        return self.size

    def save(self):
        hs = 12
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("49424143") # IBAC
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt16(buffer, 10, 65535) # Write 0xFFFF

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

class ZCAB_CABI_CE:
    'Zelda Course Arrangement Binary (.zab) Course Arangement Binary Icons Child Element'
    def __init__(self, data, num):
        self.size = len(data)
        self.data = data[:-3] # Remove 0xFF FF FF  from end

        self.unknwn1 = d.UInt32(self.data, 0)
        self.UID_ref = d.UInt8(self.data, 4)
        self.unknwn2 = d.UInt32(self.data, 5) # Probably Not a UInt32 ! ( 4x UInt8 Flags ? / Coords + Rotation)

        # TODO: Find out what the Bytes change ingame
        print("I_CE: UNKNWN1:"+str(self.unknwn1) + " UIDR:"+str(self.UID_ref) + " UNKNWN2:"+str(self.unknwn2) + "   [:"+str(num)+"] - Hex (Unknwn2): "+str(self.data[5:].hex()))

    def save(self):
        return self.data + b'\xFF\xFF\xFF'

################################################################
## .zab  (ZCAB) File END
###############################################################

def fromFile(path):
    return ZAB(d.ReadFile(path))